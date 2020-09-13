from firebase import firebase

# init
firebase = firebase.FirebaseApplication('https://lensign-wanda.firebaseio.com', authentication=None)

def minify_signature_data_pt(map, START_TIME = 0):
    return [
        map['x'],
        map['y'],
        map['pressure'],
        map['timeMs'],
    ]

class Datasets:
    def list_all(self):
        res = firebase.get('/datasets', None)
        results = []
        for key in res:
            results.append({
                'id': key,
                'name': res[key]['name']
            })
        return results

    def add(self, name):
        new_item = {
            'name': name
        }
        res = firebase.post('/datasets', new_item, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
        new_item['id'] = res['name']
        return new_item
    
    def list_signatures(self, dataset_id):
        res = firebase.get('/user_signatures/', dataset_id)
        results = []

        for key in res:
            signature = res[key]
            processed_signature = []

            START_TIME = None
            for data_pt in signature:
                if START_TIME == None:
                    START_TIME = signature[0]['timeMs']
                
                processed_signature.append(minify_signature_data_pt(data_pt, START_TIME))

            results.append({
                'id': key,
                'data_pts': processed_signature
            })
        return results

    def add_signature(self, dataset_id, new_item):
        res = firebase.post('/user_signatures/' + dataset_id, new_item, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
        return {
            'id': res['name'],
        }
    
#
# create an object for each Controller class (similar to export in JS)
#
datasets = Datasets()