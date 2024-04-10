from flask import Flask,request,jsonify,render_template
import os, datetime
import db
from models import Book


app = Flask(__name__)


## create db once
if not os.path.isfile('books.db'):
    db.connect()



## home page
@app.route('/')
def index():
    return render_template('index.html')



@app.route("/request", methods=["POST"])
def postRequest():
    req_data = request.get_json()
    email = req_data['email']
    title = req_data['title']
    bks = [b.serialize() for b in db.view()]
    for b in bks:
        if b['title'] == title:
            return jsonify({
                'res':f"Error book with title {title} is already present !!",
                'status': '404'
            })
    
    bk = Book(db.getNewId(), True, title, datetime.datetime.now())
    print("new book: ", bk.serialize())
    db.insert(bk)
    new_bks = [b.serialize() for b in db.view()]

    print ("All books : ", new_bks)

    return jsonify({
        'res': bk.serialize(),
        'status': '201',
        'msg': 'Successfully created a new book!!'
    })


@app.route('/request', methods=['GET'])
def getRequest():
    content_type = request.headers.get('Content-Type')
    bks = [b.serialize() for b in db.view()]
    if (content_type == 'application/json'):
        json = request.json
        for b in bks:
            if b['id'] == int(json['id']):
                return jsonify({
                    'res': b,
                    'status': '200',
                    'msg': 'Success getting all books from db'
                })  
        
        return jsonify({
            'error':f"Error!! book with id '{json['id']}' not found.",
            'res':' ',
            'status': '404'
        })
    else:
        return jsonify({
                    'res': bks,
                    'status': '200',
                    'msg': 'Success getting all books in library!👍😀',
                    'no_of_books': len(bks)
                })
 
@app.route('/request/<id>', methods=['GET'])
def getRequestById(id):
    req_args = request.view_args
    print('req_args:' ,req_args)

    bks = [b.serialize() for b in db.view()]

    if req_args:
        for b in bks:
            if b['id'] == int(req_args['id']):
                return jsonify({
                    'res': b,
                    'status': '200',
                    'msg': 'Success!!'
                })
        return jsonify({
            'error':f"Error!! book with id '{req_args['id']}' not found.",
            'res':' ',
            'status': '404'
        })
    else:
        return jsonify({
            'res': bks,
            'status': '200',
            'msg': 'Success getting books by id!!',
            'no_of_books': len(bks)

        })

@app.route('/request', methods=['PUT'])
def putRequest():
    req_data = request.get_json()
    available = req_data['available']
    title = req_data['title']
    id = req_data['id']
    print(req_data)
    bks = [b.serialize() for b in db.view()]

    for b in bks:
        if b['id'] == id:
            bk = Book(
                id,
                available,
                title,
                datetime.datetime.now()
            )
            print('update book:', bk.serialize())
            db.update(bk)
            print('iiiiiiiiiiiiiiiiii')
            updated_bks = [b.serialize() for b in db.view()]
            print('updated books: ', updated_bks)

            return jsonify({
                'res': bk.serialize(),
                'status': '200',
                'msg': 'Successfully updated book!'
            })
    return jsonify({
        'error':f"Error!! failed to update book with id '{req_data['id']}'.",
        'res':' ',
        'status': '404'
    })

@app.route('/request/<id>', methods=['DELETE'])
def deleteRequest(id):
    req_args = request.view_args
    print('req_args:', req_args)
    # the_id = req_args['id']
    bks = [b.serialize() for b in db.view()]

    if(req_args):
        for b in bks:
            if b['id'] == int(req_args['id']):
                db.delete(b['id'])
                updated_bks_after_del = [b.serialize() for b in db.view()]
                print('updated books after delete:', updated_bks_after_del)

                return jsonify({
                    'res': updated_bks_after_del,
                    'status': '200',
                    'msg':'book deleted successfully!!',
                    'no_of_books':len(updated_bks_after_del)
                })
    else:
        return jsonify({
            'error':f"failed to delete book with id {req_args['id']}",
            'res':'',
            'status':'404'
        })
    
@app.route('/request',methods=['DELETE'])
def deleteAllRequest():
    bks = [b.serialize() for b in db.view()]
    if (len(bks) != 0 ):
        db.deleteAll()
        n_bks = [b.serialize() for b in db.view()]
        return jsonify({
            'res': n_bks,
            'status':'200',
            'msg':'All books Deleted successfully!!',
            'no_of_books': len(n_bks)
        })
    else:
        return jsonify({
            'error': f"Error deleting books",
            'res': '',
            'status': '404'
        })


if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)   