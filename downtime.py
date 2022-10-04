!alias ashdt {{f'''{'{'}{'{'}args=&ARGS&{'}'}{'}'}'''}}
{{get_gvar("6dcda37f-276f-44bb-81ed-c74290fe0a65")}}

!alias ashdt
<drac2>
# downtime.py
using(
	embeds = '72fea181-ba03-4cb4-8edf-1f3bc5a49578'
)
gvar = load_json(get_gvar("97fdc2f7-34d4-466b-9678-019d90633f79"))
#args=&ARGS&
resource = gvar.dtresource
embed = {"title": resource.title, "desc": resource.get("desc",""), "fields": [], "thumb": resource.get("thumb",""), "footer": resource.get("footer","")}


c = character()
t = int(time())
c.set_cvar_nx("LastPing", str(t))
c.set_cvar_nx("Downtime", "0")
l = int(LastPing)
m = 0
if args:
	cmd = args[0]
	if cmd.lstrip('-+').isdigit():
		m = -int(cmd.lstrip('-+'))
		if cmd.startswith('+'): m = -m
	else:
		if cmd in "retire.no.off.null.false.pause.inactive.offline":
			l = -1
		elif cmd in "on.return.true.unpause.active.online":
			l = t
if l < 0:
	t = -1
c.set_cvar("LastPing", str(t))

if l > 0:
	a = t - l
	wk = 86400
	d = a + int(Downtime) + (m * wk)
	c.set_cvar("Downtime", str(d))
	n = t + (wk - (d % wk))
	embed.fields.append({ "title": f"Last checked", "body": f"<t:{l}:f>: <t:{l}:R>", "inline": False })
	if m:
		embed.fields.append({ "title": f"Manual Adjustment", "body": f"{'**Spent**' if m < 0 else ':warning: __**Gained**__'} {-m if m < 0 else m} downtime weeks", "inline": False })
	embed.fields.append({ "title": f"Total Available Downtime", "body": f"{d/wk:.0f} workweeks", "inline": False })
	embed.fields.append({ "title": f"Next Workweek", "body": f"Next full week <t:{n}:R> (<t:{n}:T>)", "inline": False })
else:
	embed.fields.append({ "title": f"Downtime accumulation stopped", "body": f"No downtime will be credited to this character until they return.", "inline": False })

return embeds.get_output(embed)
</drac2>