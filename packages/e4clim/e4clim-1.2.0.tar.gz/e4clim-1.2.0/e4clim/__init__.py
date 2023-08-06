"""e4clim package."""
from typing import Type
from .build.application import BuilderApplication, DirectorApplication
from .build.base import BuilderBase, DirectorBase
from .build.context_component import (BuilderContextComponent,
                                      DirectorContextComponent)
from .build.context_result import BuilderContextResult, DirectorContextResult
from .build.strategy import BuilderStrategy, DirectorStrategy
from .build.context_optimizer import (BuilderContextOptimizer,
                                      DirectorContextOptimizer)
from .context.mediator import Mediator
from .typing import PathType

# @package .
#  e4clim: Energy for CLimate Integrated Model.
#
#  e4clim: Energy for CLimate Integrated Model.

from e4clim._version import get_versions
__version__ = get_versions()['version']
del get_versions


def launch(cfg_filepath: PathType,
           provider_builder_strategy:
           Type[BuilderBase] = BuilderStrategy,
           provider_director_strategy:
           Type[DirectorBase] = DirectorStrategy,
           provider_builder_context_result:
           Type[BuilderBase] = BuilderContextResult,
           provider_director_context_result:
           Type[DirectorBase] = DirectorContextResult,
           provider_builder_context_component:
           Type[BuilderBase] = BuilderContextComponent,
           provider_director_context_component:
           Type[DirectorBase] = DirectorContextComponent,
           provider_builder_context_optimizer:
           Type[BuilderBase] = BuilderContextOptimizer,
           provider_director_context_optimizer:
           Type[DirectorBase] = DirectorContextOptimizer,
           provider_builder_application:
           Type[BuilderBase] = BuilderApplication,
           provider_director_application:
           Type[DirectorBase] = DirectorApplication) -> Mediator:
    """Launch application and return mediator.

    :param cfg_filepath: Configuration filepath.
    :param provider_builder_strategy: Strategy-builder provider.
    :param provider_director_strategy: Strategy-director provider.
    :param provider_builder_context_result: Result-context builder provider.
    :param provider_director_context_result: Result-context director provider.
    :param provider_builder_context_component: Component-context builder
      provider.
    :param provider_director_context_component: Component-context director
      provider.
    :param provider_builder_context_optimizer: Optimizer-context builder
      provider.
    :param provider_director_context_optimizer: Optimizer-context director
      provider.
    :param provider_builder_application: Application-builder provider.
    :param provider_director_application: Application-director provider.

    :returns: Mediator.
    """

    director_app = _get_director_application(
        provider_builder_strategy, provider_director_strategy,
        provider_builder_context_result, provider_director_context_result,
        provider_builder_context_component,
        provider_director_context_component,
        provider_builder_context_optimizer,
        provider_director_context_optimizer,
        provider_builder_application, provider_director_application)

    med = director_app.make(cfg_filepath)

    return med


def _get_director_application(
        provider_builder_strategy: Type[BuilderBase],
        provider_director_strategy: Type[DirectorBase],
        provider_builder_context_result: Type[BuilderBase],
        provider_director_context_result: Type[DirectorBase],
        provider_builder_context_component: Type[BuilderBase],
        provider_director_context_component: Type[DirectorBase],
        provider_builder_context_optimizer: Type[BuilderBase],
        provider_director_context_optimizer: Type[DirectorBase],
        provider_builder_application: Type[BuilderBase],
        provider_director_application:
        Type[DirectorBase]) -> Type[DirectorBase]:
    """Get application director.

    :param provider_builder_strategy: Strategy-builder provider.
    :param provider_director_strategy: Strategy-director provider.
    :param provider_builder_context_result: Result-context builder provider.
    :param provider_director_context_result: Result-context director provider.
    :param provider_builder_context_component: Component-context builder
      provider.
    :param provider_director_context_component: Component-context director
      provider.
    :param provider_builder_context_optimizer: Optimizer-context builder
      provider.
    :param provider_director_context_optimizer: Optimizer-context director
      provider.
    :param provider_builder_application: Application-builder provider.
    :param provider_director_application: Application-director provider.

    :returns: Application director.
    """
    builder_strategy = provider_builder_strategy()
    deputy_strategy = provider_director_strategy(builder_strategy)

    builder_context_result = provider_builder_context_result()
    deputy_context_result = provider_director_context_result(
        builder_context_result, deputy_strategy)

    builder_context_component = provider_builder_context_component()
    deputy_context_component = provider_director_context_component(
        builder_context_component, deputy_context_result)

    builder_context_optimizer = provider_builder_context_optimizer()
    deputy_context_optimizer = provider_director_context_optimizer(
        builder_context_optimizer)

    builder_app = provider_builder_application()
    director_app = provider_director_application(
        builder_app, deputy_context_component, deputy_context_optimizer)

    return director_app
