"""Module for Entity and entity Group data models"""
from datetime import datetime
from posixpath import join
from typing import TYPE_CHECKING, Any, Dict, Optional, cast

from pydantic import Field

from ...models import BaseModel, History, State

if TYPE_CHECKING:
    from homeassistant_api import Client


class AsyncGroup(BaseModel):
    """Represents the groups that entities belong to"""

    group_id: str
    client: "Client" = Field(exclude=True, repr=False)
    entities: Dict[str, "AsyncEntity"] = {}

    def add_entity(self, entity_slug: str, state: State) -> None:
        """Registers entities to this Group object"""
        self.entities.update(
            {entity_slug: AsyncEntity(slug=entity_slug, state=state, group=self)}
        )

    def get_entity(self, entity_slug: str) -> Optional["AsyncEntity"]:
        """Returns Entity with the given name if it exists. Otherwise returns None"""
        return self.entities.get(entity_slug)


class AsyncEntity(BaseModel):
    """Represents entities inside of homeassistant"""

    slug: str
    state: State
    group: AsyncGroup = Field(exclude=True, repr=False)

    async def async_get_state(self) -> State:
        """Asks Home Assistant for the state of the entity and sets it locally"""
        state_data = await self.group.client.async_request(
            join("states", self.entity_id)
        )
        self.state = self.group.client.process_state_json(
            cast(Dict[str, Any], state_data)
        )
        return self.state

    async def async_set_state(self, state: State) -> State:
        """Tells Home Assistant to set the given State object."""
        return await self.group.client.async_set_state(
            self.entity_id,
            group=self.group.group_id,
            slug=self.slug,
            **state.dict(),
        )

    @property
    def entity_id(self):
        """Constructs the entity_id string from its group and slug"""
        return self.group.group_id + "." + self.slug

    async def async_get_history(
        self,
        start_timestamp: Optional[datetime] = None,
        # Defaults to 1 day before. https://developers.home-assistant.io/docs/api/rest/
        end_timestamp: Optional[datetime] = None,
        minimal_state_data: bool = False,
        significant_changes_only: bool = False,
    ) -> Optional[History]:
        """Gets the previous `State`'s of the `Entity`."""
        history: Optional[History] = None
        async for history in self.group.client.async_get_entity_histories(
            entities=(self,),
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            minimal_state_data=minimal_state_data,
            significant_changes_only=significant_changes_only,
        ):
            break
        return history
