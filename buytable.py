!alias buytable <drac2>
# load tables
tables=load_json(get_gvar('6ece7972-0aff-4ce1-8760-128a13268c85'))
args=&ARGS&

# get table
t = args[0].upper() if len(args)>0 else 'none'

embed = f'embed -thumb {tables.resource.thumb} -title "{tables.resource.title}" -f '
resource = tables['resource']
alias = f'{ctx.prefix}{ctx.alias}'
footer = tables.resource.footer.replace("[alias]",alias)

if t in tables:
	meta = tables['meta'][t]
	rarity = tables['rarity']
	seek = ''
	
	if len(args)>1:
		seek = args[1].lower()
		if not (seek in rarity):
			seek_item = " ".join(args[1:])
			# lookup rarity: A-I = 
			t_seek = 'ABCDEFGHI' 
			t_id = 0 
			while t_id < len(t_seek) and not (seek in rarity):
				table=[dict(name=item.name,rarity=item.rarity) for item in tables.get(t_seek[t_id],[]) if seek_item.lower() in item.name.lower()]
				if table:
					seek = table[0].rarity
					seek_item = table[0].name
				t_id += 1
			if not (seek in rarity):
				#return err(f'Do not recognise "{seek_item}", try again or just use rarity code')	
				return f'{embed}"Error|Cannot find item \\\"{seek_item}\\\" in treasure tables, try again or just use the rarity codes" -footer "{footer}"'
				
		elif len(args)>2:
			seek_item = " ".join(args[2:])
		else:
			seek_item = ''
		seek_item = f'\\\"__{seek_item}__\\\"' if seek_item else ''
	
	t_roll = meta['roll']
	t_qty = roll(t_roll)
	t_chk = meta['check']
    header=f'Rolling for items on __Table {t}__|Found `{t_roll}` ({t_qty}) item{"s" if t_qty>1 else ""}\n　(Persuade `{t_chk}` or higher)'
    table_items=[]
	
	if seek in rarity:
		seek_roll = rarity[seek]['roll']
		seek_check = rarity[seek]['check']
		seek_name = rarity[seek]['name']
		header = f'Seeking specific item {seek_item} ({seek_name})|Buy for: __{roll(seek_roll)} gp__\n　(Persuade `{seek_check}` or higher, price `{seek_roll}`)" -f "{header}'
		
    for idx in range(t_qty):
        table=[dict(min=int(item.min),max=int(item.get('max',item.min)),name=item.name,rarity=item.rarity) for item in tables.get(t,[])]
        if table:
            die_size=max(item.max for item in table)
            item_roll=vroll(f'1d{die_size}')
            item_idx = f'**{idx + 1}.**' if t_qty > 1 else ''
            if match:=[dict(name=item.name,rarity=rarity[item.rarity]) for item in table if item_roll.total>=item.min and item_roll.total<=item.max]:
				item_name = match[0].name
				lines = item_name.split('\n')
				if len(lines)>1 and '(roll d' in lines[0].lower():
					# extract roll and subitems
					group_roll = roll(lines[0].lower().split('(roll ')[1].split(')')[0])
					for line in lines[1:]:
						vals = line.split(')',1)[0].split('-')
						if group_roll==int(vals[0]) or (len(vals)>1 and group_roll>=int(vals[0]) and group_roll<=int(vals[1])):
							item_name = f'{lines[0]}: `{group_roll}`\n　　{line}'
				item_price = roll(match[0].rarity.roll)
				item_rarity = match[0].rarity
				table_items.append(f'{item_idx} `{item_roll.total}`　**{item_name}**: __{item_price} gp__\n　　　(*{item_rarity.name} price* `{item_rarity.roll}`)')
            else:
                item_name='error'
				item_price='none'
	# format output
	nl='\n'
	return f'{embed}"{header}\n\n{nl.join(table_items)[:1024]}" -footer "{footer}"'
else:
	return f'{embed}"{tables.resource.help.replace("[alias]",alias)}" -f "{tables.resource.examples.replace("[alias]",alias)}" -footer "{footer}"'
</drac2>
