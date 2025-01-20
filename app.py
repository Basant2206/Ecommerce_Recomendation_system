# flask,pandas

from flask import Flask, request, render_template
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

#data
trending_products=pd.read_csv("models/trending_product.csv")
final_data=pd.read_csv("models/final_data.csv")
################

def content_based_recommendation(data,item_name,topn=10):
    if item_name not in data['name'].values:
        print(f"Item '{item_name}' not found in the available data")
        return pd.DataFrame()

    tfidf_vectorizer=TfidfVectorizer(stop_words='english')
    tfidf_tags_content=tfidf_vectorizer.fit_transform(data['tags'])
    cosine_similar_content=cosine_similarity(tfidf_tags_content,tfidf_tags_content)
    index_item=data[data['name']==item_name].index[0]
    similar_item=list(enumerate(cosine_similar_content[index_item]))
    similar_items=sorted(similar_item, key=lambda x:x[1],reverse=True)[1:topn+1]
    top_recomended_item=[x[0] for x in similar_items]
    recomended_items_details=data.iloc[top_recomended_item][['name','reviewCount','brand','price','imageUrl','rating']]
    return recomended_items_details

def truncate(text, length):
    if len(text) > length:
        return text[:length] + "..."
    else:
        return text

app = Flask(__name__)


print(trending_products)
# route
@app.route('/')
def index():

    return render_template('index.html',trending_products=trending_products.head(8),truncate=truncate
                           )

@app.route('/main',)
def main():
    return render_template('main.html')

@app.route('/index')
def toindex():
    return render_template('index.html')

@app.route('/recommendations', methods=['POST', 'GET'])
def recommendations(rec=None, truncate=None):
    if request.method == 'POST':
        prod=request.form.get('prod')
        nbr=request.form.get('nbr')

        content_based_rec=content_based_recommendation(final_data,prod,nbr)

        if content_based_rec.empty:
            print("hch")
            message = "No recommendations available for this product."
            return render_template('main.html', message=message)
        else:
            print(999)
            return render_template('main.html', content_based_rec=content_based_rec, truncate=truncate)


if __name__ == '__main__':
    app.run(debug=True)



