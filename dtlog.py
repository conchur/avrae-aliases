!alias dtlog tembed {{f'''{'{'}{'{'}args=&ARGS&{'}'}{'}'}'''}}
{{get_gvar("be55116b-2337-44bf-84f7-dbd4972e645c")}}



<drac2>
# dtlog.py
using(
	embeds = '72fea181-ba03-4cb4-8edf-1f3bc5a49578'
)
gvar = load_json(get_gvar("97fdc2f7-34d4-466b-9678-019d90633f79"))
#args=&ARGS&
#alias = f'{ctx.prefix}{ctx.alias}'
alias = f'!dtlog'
resource = gvar.dtlresource
embed = {"title": resource.title, "desc": resource.get("desc",""), "fields": [], "thumb": resource.get("thumb",""), "footer": resource.get("footer","").replace("<alias>", alias)}

dts = gvar['downtime']
items = gvar['items']
item = {}

c = character()
action = args[0] if args else 'help'
activity = 0
downtime = {}
wk = 86400
dtwks = int(Downtime) / wk
gold = c.coinpurse.total
embed.fields.append({ "title": f"Available Resources", "body": f":hourglass: **Downtime**: {dtwks:.0f} work-weeks\n<:DDBGold:953399505062080594> **Total Coin**: {gold:.2f} gold", "inline": False })

if action in 'help.?':
	activity = 1
elif action in 'learn.study.upskill.training':
	downtime = dts['learn']
	activity = 2
elif action in 'teacher.instructor.assist.help':
	downtime = dts['teach']
	activity = 3
elif action in 'research.formula':
	downtime = dts['research']
	activity = 4
elif action in 'ingredient.component.add':
	downtime = dts['component']
	activity = 5
elif action in 'craft.make':
	downtime = dts['craft']
	activity = 6
elif action in 'miscellaneous.scroll.wait':
	downtime = dts['misc']
	activity = 7
elif action in 'cancel.no.':
	activity = 9
elif action in 'confirm.doit.yes':
	activity = 10
elif action in 'undo.revert':
	activity = 11
elif action in 'list.history':
	activity = 12
else:
	activity = 0
	
if activity == 0:
	# arg error
	notfound = { "title": "Downtime not found", "body": resource.get("notfound","Activity not found"), "inline": False }
	embed.fields.append(notfound)
	
if downtime:
	embed.fields.append({ "title": f"{downtime.name}", "body": f"{downtime.help.replace('<alias>',alias)}", "inline": False })
	if downtime.get('example',''):
		embed.fields.append({ "title": f"Examples:", "body": f"{downtime.example.replace('<alias>',alias)}", "inline": False })
	
return embeds.get_output(embed)
</drac2>
