from flask import Flask,render_template,request,jsonify
from flask_sqlalchemy import *
from flask_marshmallow import Marshmallow
from Source.Scripts.framework.Stringsimilarity import Similarity
from Source.Scripts.framework.Recipe_prescribe import Recipe_P


from Source.Scripts.framework.StoreSimilarity import Storesim
import base64
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Produce.db'

ma = Marshmallow(app)
db = SQLAlchemy(app)

class Iceland(db.Model):
    __tablename__ = 'Iceland'
    Product_id = db.Column(db.String(), primary_key=True)
    Image_Url = db.Column(db.String())
    Image_Path = db.Column(db.String())
    Image_Data = db.Column(db.Binary())


class Aldi(db.Model):
    __tablename__ = 'Aldi'
    Product_id = db.Column(db.String(), primary_key=True)
    Image_Url = db.Column(db.String())
    Image_Path = db.Column(db.String())
    Image_Data = db.Column(db.Binary())



class Recipes(db.Model):
    __tablename__ = 'Recipes'
    Category = db.Column(db.String(), primary_key=True)
    Recipe_id = db.Column(db.String())
    Ingredients = db.Column(db.String())
    TEXT = db.Column(db.TEXT)
    Instructions = db.Column(db.String())
    Image_Url = db.Column(db.String())
    Image_Path = db.Column(db.String())
    Image_Data = db.Column(db.Binary())



class Tesco(db.Model):
    __tablename__ = 'Tesco'
    Product_id = db.Column(db.String(), primary_key=True)
    Image_Url = db.Column(db.String())
    Image_Path = db.Column(db.String())
    Image_Data = db.Column(db.Binary())



class Supervalue(db.Model):
    __tablename__ = 'Supervalue'
    Product_id = db.Column(db.String(), primary_key=True)
    Image_Url = db.Column(db.String())
    Image_Path = db.Column(db.String())
    Image_Data = db.Column(db.Binary())



class Recipes_Schema(ma.ModelSchema):
    class Meta:
        model = Recipes


class Iceland_Schema(ma.ModelSchema):
    class Meta:
        model = Iceland

class Tesco_Schema(ma.ModelSchema):
    class Meta:
        model = Tesco

class Supervalue_Schema(ma.ModelSchema):
    class Meta:
        model = Supervalue

class Aldi_Schema(ma.ModelSchema):
    class Meta:
        model = Aldi()


@app.route('/')
def index():
    return render_template('layout.html')


@app.route('/get_store',methods=['GET'])
def get_store():
    string1 = request.args.get("Store") # Gets the store associated with the string using similarity
    print(string1)
    value = Storesim(string1).actual
    return jsonify([{'Store':value}])


@app.route('/recipes',methods=['GET'])
def get_recipes():
    result = request.args.get('Products')  # gets the product from that store using similarity
    print(result)
    result = result.split(',')
    ontologies = Recipe_P(result)
    print(ontologies.recipes)
    entries = []
    for entry in ontologies.recipes[:10]:
        example = Recipes.query.filter_by(Recipe_id = entry).with_entities(Recipes.Recipe_id, Recipes.Ingredients, Recipes.Instructions).first()
        entries.append(example)

    user_schema = Recipes_Schema(many = True)
    output = user_schema.dump(entries)
    data = jsonify(output)
    return data


@app.route('/Tesco/Query',methods=['GET'])
def get_tesco_products():
    result = request.args.get('Products') # gets the product from that store using similarity
    results = result.split(',')
    products = [Similarity('Tesco', i).__str__() for i in results]
    entries = []
    for entry in products:
        example = Tesco.query.filter_by(Product_id = entry).with_entities(Tesco.Product_id, Tesco.Image_Url, Tesco.Image_Path).all()
        entries.append(example[0])
    user_schema = Tesco_Schema(many=True)

    output = user_schema.dump(entries)

    return jsonify(output)


@app.route('/Supervalue/Query',methods=['GET'])
def get_supervalue_products():
    result = request.args.get('Products') # gets the product from that store using similarity
    print(result)
    results = result.split(',')
    print(results)
    while '' in results:
        results.remove('')
    products = [(Similarity('Supervalue', i).__str__(),i) for i in results]
    entries = []
    for entry in products:
        if entry[0] != '':
            print(entry)

            example = Supervalue.query.filter_by(Product_id = entry[0]).with_entities(Supervalue.Product_id, Supervalue.Image_Url, Supervalue.Image_Path).first()
            entries.append(example)


    print(entries)
    user_schema = Supervalue_Schema(many=True)

    output = user_schema.dump(entries)
    print(output)

    return jsonify(output)


@app.route('/Aldi/Query',methods=['GET'])
def get_aldi_products():
    result = request.args.get('Products') # gets the product from that store using similarity
    results = result.split(',')
    products = [Similarity('Aldi', i).__str__() for i in results]
    entries = []
    for entry in products:
        example = Aldi.query.filter_by(Product_id = entry).with_entities(Aldi.Product_id, Aldi.Image_Url, Aldi.Image_Path).all()
        entries.append(example[0])
    user_schema = Aldi_Schema(many=True)

    output = user_schema.dump(entries)

    return jsonify(output)



@app.route('/Iceland/Query',methods=['GET'])
def get_iceland_products():
    result = request.args.get('Products') # gets the product from that store using similarity
    results = result.split(',')
    products = [Similarity('Iceland', i).__str__() for i in results]
    entries = []
    for entry in products:
        example = Iceland.query.filter_by(Product_id = entry).with_entities(Iceland.Product_id, Iceland.Image_Url, Iceland.Image_Path).all()
        entries.append(example[0])
    user_schema = Iceland_Schema(many=True)

    output = user_schema.dump(entries)

    return jsonify(output)


@app.route('/Tesco')
def list_tesco():
    example = Tesco.query.with_entities(Tesco.Product_id, Tesco.Image_Url, Tesco.Image_Path).all()
    user_schema = Tesco_Schema(many=True)
    output = user_schema.dump(example)
    data = jsonify(output)
    return data


@app.route('/Supervalu')
def list_supervalue():
    example = Supervalue.query.with_entities(Supervalue.Product_id, Supervalue.Image_Url, Supervalue.Image_Path).all()
    user_schema = Supervalue_Schema(many=True)
    output = user_schema.dump(example)
    data = jsonify(output)
    return data


@app.route('/Aldi/')
def list_aldi():
    example = Aldi.query.with_entities(Aldi.Product_id, Aldi.Image_Url, Aldi.Image_Path,Aldi.Image_Data).all()
    user_schema = Aldi_Schema(many=True)
    output = user_schema.dump(example)
    print(output)
    for i in output:
        print(i['Image_Data'])
        i['Image_Data'] = base64.encode(i['Image_Data'],'cp437')
        print(i['Image_Data'])
    #return jsonify(output)


@app.route('/Iceland')
def list_iceland():
    example = Iceland.query.with_entities(Iceland.Product_id, Iceland.Image_Url, Iceland.Image_Path).all()
    user_schema = Iceland_Schema(many=True)
    output = user_schema.dump(example)
    data = jsonify(output)
    return data



if __name__ == '__main__':
    app.run(debug=True)