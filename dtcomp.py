!alias dtcomp <drac2>
# load tables
gvar=load_json(get_gvar('860b567d-234e-42a2-972d-8507b69ba74b'))
args=&ARGS&

task = args[0].lower() if len(args)>0 else 'help'
hasqty = (len(args)>1 and args[len(args)-1].isdigit())
qty = int(args[len(args)-1]) if hasqty else 1

resource = gvar['resource']
alias = f'{ctx.prefix}{ctx.alias}'
footer = resource.footer.replace("[alias]",alias)

if qty > 7:
    return f'embed -thum {resource.thumb} -title "{resource.title}" -f "Too Many Complications|You asked for `{qty}` - to keep these messages reasonably short the maximum is 7." -footer "{footer}"'

comptask = gvar[task] if task in gvar.list else None
if not comptask:
    words = args[:len(args) - (1 if hasqty else 0)]
    if words:
        for task in gvar.list:
            comptask = gvar[task]
            for word in words:
                word = word.lower()
                if not (word in comptask.name.lower() or word in task.lower()):
                    comptask = None
                    break
            if comptask: 
                break

embed = f'embed -thumb {comptask.thumb if comptask and comptask.thumb else resource.thumb} -title "{resource.title}" -f '

if comptask:
	compcheck = comptask.get("comproll",'')
	compalways = (compcheck=="1" or compcheck.lower()=="true" or not compcheck)
	compdc = int(comptask.get("compdc",1))
	compdie = comptask.get("die",'')
	comptable = comptask.get("table")
	header = f'{comptask.name}|'
	if 'url' in comptask: header += f'[link]({comptask.url})\n'
	if 'compdesc' in comptask: header += f'{comptask.compdesc}\n\n'
	header += "(Rolling generated complications)" if compalways else f'(If `{compcheck}` does not beat {compdc}, roll {compdie} on complication table)'
	
	comprolls = 'Rolls|'
	comps = 0
	if compcheck:
		for rr in range(1,qty+1):
			
			if qty>1: comprolls += f'**{rr}**: '
			comproll = compdc if compalways else roll(compcheck)
			if comproll <= compdc:
				tableroll = roll(compdie)
				tableval = comptable[tableroll-1]
				if not compalways: comprolls += f' rolled `{comproll}`: '
				comprolls += f'**__COMPLICATION__**!\n　　(`{compdie}`) `{tableval}`\n'
				comps += 1
			else:
				comprolls += f' rolled `{comproll}`: No complication\n'
			
		if comps > 0 and '*`' in comprolls:
			comprolls += f'\n　　*Might involve a rival'
	else:
		comprolls = "No complications for this task"
		
	return f'{embed}"{header}" -f "{comprolls}" -footer "{footer}"'
else:
	return f'{embed}"{resource.help.replace("[alias]",alias)}" -f "{resource.examples.replace("[alias]",alias)}" -footer "{footer}"'
</drac2>