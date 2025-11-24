import os
import logging
import aiohttp
import json
from typing import Any, AsyncIterable, Optional, TypedDict
from typing_extensions import Unpack

from strands.models import Model
from strands.types.content import Messages
from strands.types.streaming import StreamEvent
from strands.types.tools import ToolSpec

from perplexity import Perplexity
    
from strands.types.streaming import StreamEvent

logger = logging.getLogger(__name__)

class PerplexityModel:
    def __init__(self, api_key, model_id, params=None):
        self.api_key = api_key
        self.model_id = model_id
        self.config = {"model_id": model_id, "params": params or {}}

    async def stream(self, messages:str, tool_specs=None, system_prompt=None, **kwargs):
        
        if isinstance(messages, list):
      
          cleaned = []
          
          for m in messages:
              if isinstance(m, dict):
                  role = m.get("role", "user")
                  content = m.get("content", "")
                  if isinstance(content, list):
                      # Flatten again here (for list-of-blocks)
                      content = "".join(
                          block.get("text", str(block)) for block in content if isinstance(block, dict)
                      ) if content and isinstance(content[0], dict) else str(content)
                  cleaned.append({"role": role, "content": content})
              else:
                  cleaned.append({"role": "user", "content": str(m)})
          
          messages = cleaned

        client = Perplexity(api_key=self.api_key) 

        # Optionally prepend system prompt
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})

        yield StreamEvent(messageStart={"role": "assistant"})

        stream = client.chat.completions.create(
            model=self.config["model_id"],
            messages=messages,
            stream=True,
            **self.config.get("params", {})
        )

        for chunk in stream:
            content = getattr(chunk.choices[0].delta, "content", None)
            if content:
                yield StreamEvent(contentBlockDelta={"delta": {"text": content}})
            if chunk.choices[0].finish_reason:
                break

        yield StreamEvent(messageStop={"stopReason": "end_turn"})

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


