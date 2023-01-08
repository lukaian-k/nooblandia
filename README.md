### **_directory structure_**

```
project/
├── assets/
├── database/
└── src/
    ├── cogs/
    │   ├── interactions/
	│	│	├── entertainments.py	➭	(game=/, dice=/, ship=/)
	│	│	└── music.py			➭	(play, queue, skip, stop)
    │   ├── tools/
	│	│	├── searches.py			➭	(google=/, chat_gpt=/)
	│	│	├── features.py			➭	(record=/, download=/)
	│	│	└── generators.py		➭	(password_generator=/, shortlink=/)
	│	├── system/
	│	│	└── management.py		➭	(on_command_error, help=/, clear=&, send=&, create_channel=&)
	│	└── math
	│		└── health.py			➭	(imc=/)
	├── reply
	│	└── defaults.py
    └── system/
        ├── json.py
        ├── ready.py
        └── system.py
```