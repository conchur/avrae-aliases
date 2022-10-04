!alias rolltable tembed {{f'''{'{'}{'{'}args=&ARGS&{'}'}{'}'}'''}}
{{get_gvar("86c28266-63dd-4a7b-a054-46af9386ee1e")}}

<drac2>
# rolltable.py
gvar = load_json(get_gvar("51c335ab-ed14-400a-bc57-7e05f5406022"))
if len(args) == 1 and args[0].lower() == 'list':
    tbls = 'Pick one of the following tbls (or use the short code in brackets instead):\n'
    for code in gvar['list']:
        tbl = gvar[code]
        tbls += f'\n**{tbl.name}** ({code})'
    return gvar['list_tables'].replace('{tables}',tbls)


tbl = {}
qty_roll = 0

if len(args)> 0:
    qty_roll = int(args[len(args)-1]) if args[len(args)-1].isdigit() else 1
    if (gvar.get(args[0],'')):
        tbl = gvar[args[0]]
    else:
        match = False
        words = []
        
        if ' ' in args[0]:
            words = args[0].split(' ')
        elif qty_roll > 1:
            words = args[0:len(args)-2]
        else:
            words = args
            
        for code in gvar['list']:
            tbl = gvar[code]
            match_name = tbl['name'].lower()
            match = True
            for word in words:
                match = True if word.lower() in match_name else False
                if not match: break
            if match: 
                break
        if not match: 
            tbl = {}
if not tbl:
    return gvar['not_found']

tbl_name = tbl['name']
tbl_type = tbl.get('type','Unknown type')
tbl_link = tbl.get('url','')
if tbl_link: tbl_type = f'[{tbl_type}]({tbl_link})'
tbl_desc = tbl.get('description','')
tbl_thumb = tbl.get('thumb','')
if tbl_thumb: tbl_desc += f'" -thumb "{tbl_thumb}'

#qty_roll = tbl.get('quantity_roll','')
qty_unit = tbl.get('quantity_units','units')
tbl_roll = f' -f "Multiroll|Rolling __**{qty_roll}**__ times"' if qty_roll>1 else ''

unit_roll = tbl.get('roll','')
unit_lookup = tbl.get('lookup', '')

count = {}
rolls = ''
if unit_lookup:
    for rollid in range(qty_roll):
        reroll = True
        while reroll:
            reroll = False
            unit = roll(unit_roll)
            lookup = ''
            for row in unit_lookup:
                tbl_parts = row.split(':')
                val = int(tbl_parts[0])
                if unit <= val:
                    if len(tbl_parts)>2 and tbl_parts[2]:
                        # limits
                        limit = int(tbl_parts[2])
                        total = count.get(row,0)
                        if (total >= limit and limit > 0):
                            reroll = True
                            break;
                        else:
                            count[row] = total + 1
                    lookup = tbl_parts[1]                    
                    break
        if lookup: rolls += f' -f "{unit} (`{unit_roll}`)|{lookup}|inline"'
        else: rolls += f' -f "{unit} (`{unit_roll}`)|not found|inline"'
else:
    return gvar['no_lookup']

return f'multiline\n!embed -title "{tbl_name}" -f "Description|*{tbl_type}*\n{tbl_desc}" -color dddd00 {tbl_roll}{rolls} -footer "!rolltable [tbl name] <rolls>"'
#\n!tbl "{tbl.name}"
</drac2>