!alias iprice tembed {{f'''{'{'}{'{'}args=&ARGS&{'}'}{'}'}'''}}
{{get_gvar("cbf3a9df-691c-4d92-9b7b-3e97ad7e201f")}}



<drac2>
# price.py
using(
	embeds = '72fea181-ba03-4cb4-8edf-1f3bc5a49578'
)
gvar = load_json(get_gvar("97fdc2f7-34d4-466b-9678-019d90633f79"))
#args=&ARGS&
resource = gvar.resource
embed = {"title": resource.title, "desc": resource.get("desc",""), "fields": [], "thumb": resource.get("thumb",""), "footer": resource.get("footer","")}

items = gvar['items']
item = {}
matches = []
rarities = gvar["rarity"]

if len(args)> 0:
	match = False
	for code in items:
		item = items[code]
		match_name = code
		for match in gvar['match']:
			if match.lower() in code.lower():
				match_name = match_name.replace(match, f"{match} {gvar['match'][match]}")
		match_name = f'{match_name} {str(item)}'.lower()
		match = True
		for word in args:
			match = True if word.lower() in match_name else False
			if not match: break
		if match:
			item['name'] = code
			matches.append(item.copy())
			#break
	if not match: 
		item = {}
if len(matches)==0:
	notfound = { "title": "Item not found", "body": resource.get("notfound","Item not found"), "inline": False }
	embed.fields.append(notfound)
elif len(matches)==1:
	item = matches[0]
	item_name = item['name']
	embed["title"] = item_name
	
	item_rarity = item.get('r','Unknown rarity')
	rarity = rarities.get(item_rarity,"")
	if rarity: item_rarity = rarity.get("n", item_rarity)

	item_type = item.get('c','Unknown type')
	item_link = "https://ddb.ac/magic-items/" + item.get('u',f"{item_name.lower().split(' (')[0].rstrip().replace(' ','-')}")
	item_source = f"*{item['s']}*" if 's' in item else ''
	item_type = f'*{item_rarity}, {item_type} ({item_source})*'
	item_uses = f"　:low_battery:  **Consumable - Number of Uses**: *{item['n']}*\n" if 'n' in item else ''
	item_attune = f"　:small_blue_diamond:  **Attunement**: *{item['a']}*\n" if 'a' in item else ''
	item_spell = f"　:small_blue_diamond:  **Spell DC**: *{item['d']}*\n" if 'd' in item else ''
	item_bonus = f"　:small_blue_diamond:  **Attack Bonus**: *{item['b']}*\n" if 'b' in item else ''
	item_desc = f"\n{item['t']}\n" if 't' in item else ''
	item_thumb = item.get('i','')
	if item_thumb:
		embed["thumb"] = item_thumb
	
	item_price = item["p"]
	embed.fields.append({ "title": f"Purchase Price", "body": f"{item_price} gp", "inline": False })
	
	item_dt = item.get('dt','')
	if item_dt:
		embed.fields.append({ "title": f"Crafting", "body": f"{item_dt}", "inline": False })
	
	item_limit = ''
	if rarity:
		item_limit = f"　:warning: **Level Requirement**: {rarity['l']}\n" if 'l' in rarity else ''
		if 't' in rarity:
			embed.fields.append({ "title": f"Magic Item Tokens", "body": f"{rarity['t']} Tokens from Season Adventures", "inline": False })

		if not item_dt:
			# <:dot:1021910347629727824> - orange
			# <:dot1:1021643622925471794> -red
			craft_time = rarity.get("ct","").replace('p',item_price)
			#craft_price = rarity.get("cp","").replace('p',item_price)
			craft_price = int(item_price)/2 if rarity.get("cp","") == "p/2" else rarity.get("cp","").replace('p',item_price)
			craft_formula = rarity.get("cf","")
			craft_ingrs = rarity.get("ci","")
			craft_dc = rarity.get("d","")
			craft_cr = rarity.get("cr","")
			if craft_time:
				embed.fields.append({ "title": f"Crafting", "body": f"<:dot:1021910347629727824> __Time__: {craft_time} downtime weeks\n<:dot:1021910347629727824> __Raw material price__: {craft_price:.0f} gp", "inline": False })
			if craft_formula:
				embed.fields.append({ "title": f"Formula", "body": f"<:dot:1021910347629727824> __Time to obtain__: {craft_formula} downtime weeks\n<:dot:1021910347629727824> __DC to obtain__: {craft_dc} (with proficient Artisan's tools)\n<:dot:1021910347629727824> __Exotic components__: {craft_ingrs} of **CR {craft_cr}**", "inline": False })

	embed["desc"] = f"[{item_type}]({item_link})\n{item_limit}{item_attune}{item_spell}{item_bonus}{item_uses}{item_desc}"
	
	item_thumb = item.get('thumb','')
	if item_thumb: 
		#item_desc += f'" -thumb "{item_thumb}'
		embed["thumb"] = item_thumb
else:
	items = ''
	for item in matches:
		items += f"<:dot1:1021643622925471794> {item['name']} ({item['s']})\n"
	embed.fields.append({ "title": f"Multiple matches found: {args}", "body": f"{items}", "inline": False })
		
return embeds.get_output(embed)
</drac2>