### **_directory structure_**

```
project/
├── assets/
├── database/
└── src/
    ├── cogs/
    │   ├── interactions/
	│	│	├── entertainments.py
	│	│	└── music.py
    │   ├── tools/
	│	│	├── searches.py
	│	│	├── features.py
	│	│	└── generators.py
	│	├── system/
	│	│	└── management.py
	│	└── math
	│		└── health.py
	├── reply
	│	└── defaults.py
    └── system/
        ├── json.py
        ├── ready.py
        └── system.py
```

### **_cogs methods_**

```
entertainments.py 	➭	(game=??, dice=/&, ship=/)
music.py			➭	(play??, queue??, skip??, stop??)
searches.py			➭	(google=/&, chat_gpt=/)
features.py			➭	(record=/&, download=/)
generators.py		➭	(password_generator=&, shortlink=/&, dall_e2=/)
management.py		➭	(help=/&, clear=/&, send=&, create_channel=&)
health.py			➭	(imc=/)
```