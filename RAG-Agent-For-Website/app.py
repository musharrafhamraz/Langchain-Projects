from flask import Flask, jsonify, render_template, request
from rag_agent.data_loader import products
from rag_agent.rag_service import WebRag
import os

app = Flask(__name__)
rag = WebRag(product_data=products)

ITEMS_PER_PAGE = 6

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    start_idx = (page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    
    total_pages = (len(products) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    current_products = products[start_idx:end_idx]
    
    return render_template('home.html', 
                         products=current_products,
                         current_page=page,
                         total_pages=total_pages)

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question')
    if not user_question:
        return jsonify({'answer': 'No question provided.'}), 400
    answer = rag.query(user_question)
    return jsonify({'answer': answer})

@app.route('/item/<int:item_id>')
def item_details(item_id):
    product = next((p for p in products if p['id'] == item_id), None)
    if product is None:
        return "Product not found", 404
    return render_template('item_details.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)