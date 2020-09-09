from firebase import firebase

# init
firebase = firebase.FirebaseApplication('https://lensign-wanda.firebaseio.com', authentication=None)

class Datasets:
    def get_all(self):
        res = firebase.get('/datasets', None)
        results = []
        for key in res:
            results.append({
                'id': key,
                'name': res[key]['name']
            })
        return results

    def new(self, name):
        new_item = {
            'name': name
        }
        res = firebase.post('/datasets', new_item, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
        new_item['id'] = res['name']
        return new_item
    
#
# create an object for each Controller class (similar to export in JS)
#
datasets = Datasets()