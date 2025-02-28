import re
from ..extranetwork_param import ExtraNetworksParam

TRIGGER = "edit"


class PromptEdit:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "positive_prompt": (
                    "STRING",
                    {"multiline": True, "forceInput": True},
                ),
                "negative_prompt": (
                    "STRING",
                    {"multiline": True, "forceInput": True},
                ),
            }
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "positive_prompt",
        "negative_prompt",
    )
    FUNCTION = "process"
    CATEGORY = "prompt-config"

    def process(self, **kwargs):
        for key in ("positive_prompt", "negative_prompt"):
            replaced_prompt, extra_networks = ExtraNetworksParam.parse(
                prompt=kwargs[key], target=[TRIGGER]
            )
            kwargs[key] = replaced_prompt

            if TRIGGER in extra_networks:
                addprompts = extra_networks[TRIGGER]

                for addprompt in addprompts:
                    if len(addprompt.positional) < 1:
                        print(f"invalid {TRIGGER} parameter length")
                        continue

                    if addprompt.positional[0] == "add":
                        to = "negative_prompt"
                        if "to" in addprompt.named:
                            if addprompt.named["to"] == "positive":
                                to = "positive_prompt"
                            elif addprompt.named["to"] == "negative":
                                to = "negative_prompt"
                            else:
                                raise ValueError("invalid 'to' option")

                        position = "tail"
                        if "position" in addprompt.named:
                            if addprompt.named["position"] == "head":
                                position = "head"
                            elif addprompt.named["position"] == "tail":
                                position = "tail"
                            else:
                                raise ValueError("invalid 'position' option")

                        prompt = ""
                        if "prompt" in addprompt.named:
                            prompt = addprompt.named["prompt"]

                        # print(f"to={to} position={position} prompt={prompt}")
                        if position == "head":
                            kwargs[to] = prompt + kwargs[to]
                        elif position == "tail":
                            kwargs[to] = kwargs[to] + prompt
                        else:
                            raise ValueError("invalid 'position' status")

                    elif addprompt.positional[0] == "replace":
                        if "pattern" not in addprompt.named:
                            raise ValueError("pattern not found")
                        if "replace" not in addprompt.named:
                            raise ValueError("replace not found")
                        kwargs[key] = re.sub(
                            pattern=addprompt.named["pattern"],
                            repl=addprompt.named["replace"],
                            string=kwargs[key],
                        )

                    else:
                        raise ValueError(
                            f"unknown {TRIGGER} mode: {addprompt.positional[0]}"
                        )

        # print(f"kwargs: {kwargs}")
        return (
            kwargs["positive_prompt"],
            kwargs["negative_prompt"],
        )


NODE_CLASS_MAPPINGS = {"PromptEdit": PromptEdit}
NODE_DISPLAY_NAME_MAPPINGS = {"Prompt": "PromptEdit"}
