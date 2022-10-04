!alias rollitem multiline 
{{f'''{'{'}{'{'}args=&ARGS&{'}'}{'}'}'''}}
{{f'''{'{'}{'{'}gvar = load_json(get_gvar("201cc7bd-8db2-4c9b-bf95-3c93abf73ab5")){'}'}{'}'}'''}}
!tembed -f "Test"
{{get_gvar("16a6794d-e3cf-4acc-bc3b-6ed67978d6d0")}}

# -- GVAR 16a6794d-e3cf-4acc-bc3b-6ed67978d6d0 --

<drac2>
# rollitem.py
if len(args) == 1 and args[0].lower() == 'list':
    items = 'Pick one of the following items (or use the short code in brackets instead):\n'
    for code in gvar['list']:
        item = gvar[code]
        items += f'\n**{item.name}** ({code})'
    return gvar['list_items'].replace('{items}',items)

item = {}
if len(args) == 1 and gvar.get(args[0],''):
    item = gvar[args[0]]
elif len(args)> 0:
    match = False
    for code in gvar['list']:
        item = gvar[code]
        match_name = item['name'].lower()
        match = True
        for word in args:
            match = True if word.lower() in match_name else False
            if not match: break
        if match: 
            break
    if not match: 
        item = {}
if not item:
    return gvar['not_found']

item_name = item['name']
item_type = item.get('type','Unknown type')
item_link = item.get('url','')
if item_link: item_type = f'[{item_type}]({item_link})'
item_desc = item.get('description','')
item_thumb = item.get('thumb','')
if item_thumb: item_desc += f'" -thumb "{item_thumb}'

qty_roll = item.get('quantity_roll','')
qty_unit = item.get('quantity_units','units')
qty = roll(qty_roll) if qty_roll else 1
item_roll = f'__**{qty}**__ {qty_unit} (`{qty_roll}`)' if qty_roll else 'item'

unit_roll = item.get('roll','')
unit_lookup = item.get('lookup', '')
item_lookup = f'| `{unit_roll}` on table ({len(unit_lookup)} rows) - please wait...' if unit_roll else ''
item_roll_type = 'Rolling for' if unit_roll and qty_roll else 'Rolled'

nested = {}
count = {}
rolls = ''
if unit_lookup:
    for rollid in range(qty):
        reroll = True
        while reroll:
            reroll = False
            unit = roll(unit_roll)
            lookup = ''
            for row in unit_lookup:
                item_parts = row.split(':')
                val = int(item_parts[0])
                if unit <= val:
                    if len(item_parts)>2 and item_parts[2]:
                        # limits
                        limit = int(item_parts[2])
                        total = count.get(row,0)
                        if (total >= limit and limit > 0):
                            reroll = True
                            break;
                        else:
                            count[row] = total + 1
                    if len(item_parts)>3 and item_parts[3]:
                        #nested
                        nested[item_parts[3]] = nested.get(item_parts[3],0) + 1
                    lookup = item_parts[1]                    
                    break
        if lookup: rolls += f' -f "{unit} (`{unit_roll}`)|{lookup}|inline"'
        else: rolls += f' -f "{unit} (`{unit_roll}`)|not found|inline"'
if rolls: rolls =f'\n!embed -f "{item_name}: {qty_unit}|Rolling {qty} {qty_unit}..." -color dd0000 {rolls}'

if nested:
    for key in nested:
        qty = nested[key]
        item = gvar.get(key,'')
        if item:
            nested_rolls = ''
            nested_name = item['name']
            unit_lookup = item.get('lookup', '')
            unit_roll = item.get('roll','')
            for rollid in range(qty):
                unit = roll(unit_roll)
                lookup = ''
                for row in unit_lookup:
                    item_parts = row.split(':')
                    val = int(item_parts[0])
                    if unit <= val:
                        lookup = item_parts[1]                    
                        break
                if lookup: nested_rolls += f' -f "{unit} (`{unit_roll}`)|{lookup}|inline"'

            if nested_rolls:
                rolls =f'{rolls}\n!embed -f "{item_name}: {nested_name}|Rolling {qty} {key}" -color dd00dd {nested_rolls}'

return f'!embed -title "{item_name}" -f "Description|*{item_type}*\n{item_desc}" -color dddd00 -f "{item_roll_type} {item_roll}{item_lookup}"{rolls} -footer "!rollitem [item name]"'
#\n!item "{item.name}"
</drac2>