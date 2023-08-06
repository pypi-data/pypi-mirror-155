# minitk

Minimalist non blocking control panel for parameters


## Installation
```
sudo apt install python3-tk
pip install minitk
```

## Usage
Here is a simple example:
```
import minitk

def say_hello():
    print('hello')

control_panel = minitk.ControlPanel()
control_panel.create_button('Say hello', say_hello)
control_panel.create_check_button('Status')
control_panel.create_slider('Value', 0, 10)
control_panel.create_menu('Options', ['a', 'b', 'c'])

while True:
    control_panel.update()

```

More examples are available under examples/