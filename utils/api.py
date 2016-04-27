from riotwatcher import RiotWatcher, RateLimit

#watcher = RiotWatcher('96a7f2b9-8718-44e3-b5f9-d6316ffc47e3')

keys = ['03351eab-47cc-4a7f-97e0-af22a7c43782', 'b7f9571e-eeef-4c8d-a5a8-cb835a6f940d', '96a7f2b9-8718-44e3-b5f9-d6316ffc47e3']

watchers = [RiotWatcher(key, limits=(RateLimit(10, 10), )) for key in keys]

def get_watcher():
	while not watchers[0].can_make_request():
		temp = watchers.pop(0)
		watchers.append(temp)
	return watchers[0]
