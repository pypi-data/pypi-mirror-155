# Copyright 2021 AIPlan4EU project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""This module defines the conditional effects remover class."""


import unified_planning as up
import unified_planning.engines as engines
from unified_planning.engines.mixins.compiler import CompilationKind, CompilerMixin
from unified_planning.engines.results import CompilerResult
from unified_planning.exceptions import UPProblemDefinitionError
from unified_planning.model import Problem, ProblemKind
from unified_planning.walkers import Simplifier
from unified_planning.engines.compilers.utils import get_fresh_name, check_and_simplify_preconditions, check_and_simplify_conditions, replace_action
from typing import Iterable, List, Dict, Tuple, Union, Optional
from itertools import chain, combinations
from functools import partial


class ConditionalEffectsRemover(engines.engine.Engine, CompilerMixin):
    '''Conditional effect remover class: this class offers the capability
    to transform a conditional problem into an unconditional one.

    This is done by substituting every conditional action with different
    actions representing every possible branch of the original action.

    Also the conditional timed_effects are removed maintaining the same
    semanthics. When this is not possible, an exception is raised.'''

    @property
    def name(self):
        return 'cerm'

    @staticmethod
    def supported_kind() -> ProblemKind:
        supported_kind = ProblemKind()
        supported_kind.set_problem_class('ACTION_BASED') # type: ignore
        supported_kind.set_typing('FLAT_TYPING') # type: ignore
        supported_kind.set_typing('HIERARCHICAL_TYPING') # type: ignore
        supported_kind.set_numbers('CONTINUOUS_NUMBERS') # type: ignore
        supported_kind.set_numbers('DISCRETE_NUMBERS') # type: ignore
        supported_kind.set_fluents_type('NUMERIC_FLUENTS') # type: ignore
        supported_kind.set_fluents_type('OBJECT_FLUENTS') # type: ignore
        supported_kind.set_conditions_kind('NEGATIVE_CONDITIONS') # type: ignore
        supported_kind.set_conditions_kind('DISJUNCTIVE_CONDITIONS') # type: ignore
        supported_kind.set_conditions_kind('EQUALITY') # type: ignore
        supported_kind.set_conditions_kind('EXISTENTIAL_CONDITIONS') # type: ignore
        supported_kind.set_conditions_kind('UNIVERSAL_CONDITIONS') # type: ignore
        supported_kind.set_effects_kind('CONDITIONAL_EFFECTS') # type: ignore
        supported_kind.set_effects_kind('INCREASE_EFFECTS') # type: ignore
        supported_kind.set_effects_kind('DECREASE_EFFECTS') # type: ignore
        supported_kind.set_time('CONTINUOUS_TIME') # type: ignore
        supported_kind.set_time('DISCRETE_TIME') # type: ignore
        supported_kind.set_time('INTERMEDIATE_CONDITIONS_AND_EFFECTS') # type: ignore
        supported_kind.set_time('TIMED_EFFECT') # type: ignore
        supported_kind.set_time('TIMED_GOALS') # type: ignore
        supported_kind.set_time('DURATION_INEQUALITIES') # type: ignore
        supported_kind.set_simulated_entities('SIMULATED_EFFECTS') # type: ignore
        return supported_kind

    @staticmethod
    def supports(problem_kind):
        return problem_kind <= ConditionalEffectsRemover.supported_kind()

    @staticmethod
    def supports_compilation(compilation_kind: CompilationKind) -> bool:
        return compilation_kind == CompilationKind.CONDITIONAL_EFFECTS_REMOVING

    def _powerset(self, iterable: Iterable) -> Iterable:
        "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

    def compile(self, problem: 'up.model.AbstractProblem',
                compilation_kind: 'up.engines.CompilationKind') -> CompilerResult:
        if not self.supports(problem.kind):
            raise up.exceptions.UPUsageError('This compiler cannot handle this kind of problem!')
        assert isinstance(problem, Problem)
        if not self.supports_compilation(compilation_kind):
            raise up.exceptions.UPUsageError('This compiler cannot handle this kind of compilation!')

        env = problem.env
        simplifier = Simplifier(env)

        new_to_old = {}

        new_problem = problem.clone()
        new_problem.name = f'{self.name}_{problem.name}'
        new_problem.clear_timed_effects()
        for t, el in problem.timed_effects.items():
            for e in el:
                if e.is_conditional():
                    f, v = e.fluent.fluent(), e.value
                    if not f.type.is_bool_type():
                        raise UPProblemDefinitionError(f'The condition of effect: {e}\ncould not be removed without changing the problem.')
                    else:
                        em = env.expression_manager
                        c = e.condition
                        nv = simplifier.simplify(em.Or(em.And(c, v), em.And(em.Not(c), f)))
                        new_problem.add_timed_effect(t, e.fluent, nv)
                else:
                    new_problem._add_effect_instance(t, e.clone())
        new_problem.clear_actions()
        for ua in problem.unconditional_actions:
            new_uncond_action = ua.clone()
            new_problem.add_action(new_uncond_action)
            new_to_old[new_uncond_action] = ua
        for action in problem.conditional_actions:
            if isinstance(action, up.model.InstantaneousAction):
                cond_effects = action.conditional_effects
                for p in self._powerset(range(len(cond_effects))):
                    new_action = action.clone()
                    new_action.name = get_fresh_name(new_problem, action.name)
                    new_action.clear_effects()
                    for e in action.unconditional_effects:
                        new_action._add_effect_instance(e.clone())
                    for i, e in enumerate(cond_effects):
                        if i in p:
                            # positive precondition
                            new_action.add_precondition(e.condition)
                            ne = up.model.Effect(e.fluent, e.value, env.expression_manager.TRUE(), e.kind)
                            new_action._add_effect_instance(ne)
                        else:
                            #negative precondition
                            new_action.add_precondition(env.expression_manager.Not(e.condition))
                    #new action is created, then is checked if it has any impact and if it can be simplified
                    if len(new_action.effects) > 0:
                        action_is_feasible, simplified_preconditions = check_and_simplify_preconditions(new_problem, new_action, simplifier)
                        if action_is_feasible:
                            new_action._set_preconditions(simplified_preconditions)
                            new_to_old[new_action] = action
                            new_problem.add_action(new_action)
            elif isinstance(action, up.model.DurativeAction):
                timing_cond_effects: Dict['up.model.Timing', List['up.model.Effect']] = action.conditional_effects
                cond_effects_timing: List[Tuple['up.model.Effect', 'up.model.Timing']] = [(e, t) for t, el in timing_cond_effects.items() for e in el]
                for p in self._powerset(range(len(cond_effects_timing))):
                    new_action = action.clone()
                    new_action.name = get_fresh_name(new_problem, action.name)
                    new_action.clear_effects()
                    for t, el in action.unconditional_effects.items():
                        for e in el:
                            new_action._add_effect_instance(t, e.clone())
                    for i, (e, t) in enumerate(cond_effects_timing):
                        if i in p:
                            # positive precondition
                            new_action.add_condition(t, e.condition)
                            ne = up.model.Effect(e.fluent, e.value, env.expression_manager.TRUE(), e.kind)
                            new_action._add_effect_instance(t, ne)
                        else:
                            #negative precondition
                            new_action.add_condition(t, env.expression_manager.Not(e.condition))
                    #new action is created, then is checked if it has any impact and if it can be simplified
                    if len(new_action.effects) > 0:
                        action_is_feasible, simplified_conditions = check_and_simplify_conditions(new_problem, new_action, simplifier)
                        if action_is_feasible:
                            new_action.clear_conditions()
                            for interval, c in simplified_conditions:
                                new_action.add_condition(interval, c)
                            new_to_old[new_action] = action
                            new_problem.add_action(new_action)
            else:
                raise NotImplementedError

        return CompilerResult(new_problem, partial(replace_action, map=new_to_old), self.name)
