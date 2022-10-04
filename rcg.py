!alias rcg tembed {{f'''{'{'}{'{'}args=&ARGS&{'}'}{'}'}'''}}
{{get_gvar("7ddcd4b7-bbc3-4495-ba9e-7f99c1aa630e")}}

# -- GVAR 7ddcd4b7-bbc3-4495-ba9e-7f99c1aa630e --
#!alias rcg embed <drac2>

<drac2>
# rcg.py
gvar = load_json(get_gvar("d47ffe01-588a-4799-b3cd-a4bb0a8664de"))
#args = &ARGS&
sections = ["race","class","background","alignment"]
subsections = ["variant","subclass","version",'trait','ideal','flaw']

resource = gvar['resource']
alias = f'{ctx.prefix}{ctx.alias}'
title = resource.title
thumb = resource.thumb
footer = resource.footer
desc = resource.desc
output = resource.help + '" -f "' + resource.examples

subsection = None
match = None
if len(args) == 0 or args[0].lower() == 'all':
    # do all
    output = "\n\n*Rolling all sections...*"
elif len(args) > 0:
    lookup = args[0].lower()
    part = 0
    if lookup == 'help':
        part = 1
    elif lookup in sections:
        part = 2
    elif lookup in subsections:
        part = 3
        
    if not part:
        for option in sections:
            if lookup in option:
                lookup = option
                part = 2
                break
    if not part:
        for option in subsections:
            if lookup in option:
                part = 3
                lookup = option
                break
        
    if part == 2:
        sections = [ lookup ]
        output = f'\n\n*Rolling for `{lookup}`...*'
    elif part == 3 and len(args) > 1:
        subsection = lookup
        if subsection == 'variant': 
            lookup = 'race'
        elif subsection == 'subclass': 
            lookup = 'class'
        else: 
            lookup = 'background'
        match = args[1].lower()
        sections = [ lookup ]
        output = f'\n\n*Rolling for `{subsection}` using filter `{lookup}: {match}`...*'
    else:
        # help
        sections = None
        if lookup and lookup != 'help':
            output += f'" -f "Section not found: `{section}`|{resource.not_found}'

if sections:
    for section in sections:
        section = gvar[section]
        options = section.roll
        rolled = None
        subrolled = None
        
        if (match):
            for option in options:
                if match in option.name.lower():
                    rolled = option
                    break
        else:
            rolled = options[roll(f'd{len(options)}')-1]
        if rolled:
            if subsection and rolled.get(subsection):
                # roll single subsection
                sub = rolled[subsection]
                subrolled = sub[roll(f'd{len(sub)}')-1]
                subdesc = section.subdesc.replace('[match]',rolled.name).replace('[subsection]',subsection)
                output += f'" -f "{subdesc}[{rolled.name}]({rolled.url}) {subsection}: **__{subrolled}__**'
            else:
                subs = ""
                # roll all subsections
                for subroll in subsections:
                    if rolled.get(subroll):
                        sub = rolled[subroll]
                        if len(sub) > 1:
                            subrolled = sub[roll(f'd{len(sub)}')-1]
                            subs += f', {subroll}: **{subrolled}**'
                output += f'" -f "{section.desc}**__[{rolled.name}]({rolled.url})__**{subs}' if rolled.get('url') else f'" -f "{section.desc}**__{rolled.name}__**{subs}'
            if rolled.get('thumb'):
                thumb = rolled.thumb
    
embed = f'-title "{title}" -desc "{desc}{output}" -thumb {thumb} -color dddd00 -footer "{footer}"'
return embed.replace("[alias]",alias)
</drac2>