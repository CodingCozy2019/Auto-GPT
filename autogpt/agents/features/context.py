from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..base import BaseAgent

from autogpt.llm.base import Message
from autogpt.models.context_item import ContextItem


class AgentContext:
    items: list[ContextItem]

    def __init__(self, items: list[ContextItem] = []):
        self.items = items

    def __bool__(self) -> bool:
        return len(self.items) > 0

    def __contains__(self, item: ContextItem):
        return any([i.source == item.source for i in self.items])

    def add(self, item: ContextItem) -> None:
        self.items.append(item)

    def close(self, index: int) -> None:
        self.items.pop(index - 1)

    def clear(self) -> None:
        self.items.clear()

    def format_numbered(self) -> str:
        return "\n\n".join([f"{i}. {c}" for i, c in enumerate(self.items, 1)])


class ContextMixin:
    """Mixin that adds context support to a BaseAgent subclass"""

    context: AgentContext

    def __init__(self, **kwargs):
        self.context = AgentContext()

        super(ContextMixin, self).__init__(**kwargs)

    def construct_base_prompt(self, *args, **kwargs):
        if kwargs.get("append_messages") is None:
            kwargs["append_messages"] = []

        if self.context:
            kwargs["append_messages"].insert(
                0, Message("system", "# Context\n" + self.context.format_numbered())
            )

        return super(ContextMixin, self).construct_base_prompt(*args, **kwargs)


def get_agent_context(agent: BaseAgent) -> AgentContext | None:
    if isinstance(agent, ContextMixin):
        return agent.context

    return None
