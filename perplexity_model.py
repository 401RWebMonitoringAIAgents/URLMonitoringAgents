import os
import logging
import aiohttp
from typing import Any, AsyncIterable, Optional, TypedDict
from typing_extensions import Unpack

from strands.models import Model
from strands.types.content import Messages
from strands.types.streaming import StreamEvent
from strands.types.tools import ToolSpec

logger = logging.getLogger(__name__)

class PerplexityModel(Model):

    class ModelConfig(TypedDict):
        model_id: str
        params: Optional[dict[str, Any]]

    def __init__(self, api_key: str, **model_config) -> None:
      
        self.api_key = api_key
        self.config = PerplexityModel.ModelConfig(**model_config)
        logger.debug("config=<%s> | initializing", self.config)

    def update_config(self, **model_config: Unpack[ModelConfig]) -> None:
        self.config.update(model_config)

    def get_config(self) -> ModelConfig:
        return self.config

    async def stream(
    self,
    messages: Messages,
    tool_specs: Optional[list[ToolSpec]] = None,
    system_prompt: Optional[str] = None,
    **kwargs: Any
  ) -> AsyncIterable[StreamEvent]:
      # Ensure messages is a list of dicts
      assert isinstance(messages, list) and isinstance(messages[0], dict)

      request = {
          "model": self.config["model_id"],
          "messages": messages,
          "params": self.config.get("params") or {}
      }
      if system_prompt:
          request["system_prompt"] = system_prompt

      headers = {
          "Authorization": f"Bearer {self.api_key}",
          "Content-Type": "application/json"
      }
      api_url = "https://api.perplexity.ai/chat/completions"
      async with aiohttp.ClientSession() as session:
          async with session.post(api_url, json=request, headers=headers) as resp:
              resp.raise_for_status()
              async for line in resp.content:
                  yield self._parse_stream_event(line)


    def _parse_stream_event(self, line):
        # Convert received chunk into a StreamEvent
        # You will need to adapt this to match Perplexity's streaming API response
        return {"contentBlockDelta": {"delta": {"text": line.decode()}}}

    async def structured_output(
      self,
      output_model,
      prompt,
      system_prompt=None,
      **kwargs
  ):

      print("structured_output was called, but it is not implemented for PerplexityModel.")
      return None


