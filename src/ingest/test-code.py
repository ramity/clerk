import re
import requests
import json

text = """TESTING :)

Save the response of a coding prompt to a variable.
{{ code hello_world Generate a simple hello world python program that additionally has a few helpful debug methods. }}

Save a variable to a file.
{{ save hello_world /tmp/hello-world.py }}

Load a line of a file into a variable.
{{ load hello_world /tmp/hello-world.py[0] }}

Load all lines of a file after a specific line into a variable.
{{ load hello_world /tmp/hello-world.py[0:] }}

Load all lines of a file up to a specific line into a variable.
{{ load hello_world /tmp/hello-world.py[:10] }}

Load a sliced selection of lines of a file into a variable.
{{ load hello_world /tmp/hello-world.py[0:10] }}

Load a complete file into a variable.
{{ load hello_world /tmp/hello-world.py }}

Use a variable within a prompt.
{{ code fibonacci Using the following python file, add an additional method that generates the fibonacci sequence:

```
$hello_world
```
}}

{{ save fibonacci /tmp/fibonacci.py }}
"""

# Memory object for extraction process.
lookup = {}

# Define regex variables.
extraction_regex = r"{{\s*(\S*)\s(\S*)\s(.*?)\s*}}"
extraction_pattern = re.compile(extraction_regex, re.DOTALL)
extraction_matches = extraction_pattern.finditer(text)

variable_substitution_regex = r"\$(\S*)"
variable_substitution_pattern = re.compile(variable_substitution_regex)

slice_regex = r"(\S*)(\[(\d*)\]|\[(\d*):\]|\[:(\d*)\]|\[(\d*):(\d*)\])"
slice_pattern = re.compile(slice_regex)

code_markdown_regex = r"```\S*\n*"
code_markdown_pattern = re.compile(code_markdown_regex)

for extraction_match in extraction_matches:

    # Get start and end index for full match
    extraction_match_start_index = extraction_match.start(0)
    extraction_match_end_index = extraction_match.end(0)

    command = extraction_match.group(1)
    variable_name = extraction_match.group(2)
    argument = extraction_match.group(3)

    print(command, variable_name, argument)

    if command == "code":

        # Perform any variable substitutions present in the argument string.
        variable_substitution_matches = variable_substitution_pattern.finditer(argument)
        for variable_substitution_match in variable_substitution_matches:
            variable_substitution_match_start_index = variable_substitution_match.start(0)
            variable_substitution_match_end_index = variable_substitution_match.end(0)
            argument = str(argument[:variable_substitution_match_start_index]) + str(lookup[variable_substitution_match.group(1)]) + str(argument[variable_substitution_match_end_index:])

        # Prefix with coding prompt limit
        argument = "Return only code without additional explanation. " + argument
        print(argument)

        # Perform the ollama request and store the response into the specified variable key.
        data = { "model": "qwen2:72b", "stream": False, "prompt": argument }
        response = requests.post("http://clerk_ollama:11434/api/generate", data=json.dumps(data))
        response_obj = json.loads(response.text)
        
        # Remove leading and trailing code markdown from response.
        response_text = response_obj["response"]
        response_text = code_markdown_pattern.sub("", response_text)

        # Make sure there's a newline at the end of the file.
        if not response_text.endswith("\n"):
            response_text += "\n"

        # Slice off the leading and trailing code markdown lines.
        lookup[variable_name] = response_text

    elif command == "save":

        # Save the contents of a specified variable into a file.
        with open(argument, "w") as file:
            file.write(lookup[variable_name])

    elif command == "load":

        # Perform slice extraction.
        slice_match = slice_pattern.search(argument)

        # Handle absence of slice definition case.
        if not slice_match:
            with open(argument, "r") as file:
                lookup[variable_name] = "".join(file.readlines())

        # Handle single index slice case.
        elif slice_match.group(3) is not None:
            with open(slice_match.group(1), "r") as file:
                lookup[variable_name] = "".join(file.readlines()[int(slice_match.group(3))])

        # Handle all after index slice case.
        elif slice_match.group(4) is not None:
            with open(slice_match.group(1), "r") as file:
                lookup[variable_name] = "".join(file.readlines()[int(slice_match.group(4)):])

        # Handle all before index slice case.
        elif slice_match.group(5) is not None:
            with open(slice_match.group(1), "r") as file:
                lookup[variable_name] = "".join(file.readlines()[:int(slice_match.group(5))])

        # Handle pair indicies slice case.
        elif slice_match.group(6) is not None and slice_match.group(7) is not None:
            with open(slice_match.group(1), "r") as file:
                lookup[variable_name] = "".join(file.readlines()[int(slice_match.group(6)):int(slice_match.group(7))])

        else:
            print("Unhandled slice.")

    else:

        print("Unhandled command.")
