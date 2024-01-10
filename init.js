conn = new Mongo();
db = conn.getDB("blog");

db.blog.createIndex({ "id": 1 }, { unique: true });

// Array of documents to be inserted
var documentsToInsert = [
    {
        "author": "Lior Milliger",
        "body": "<p>Nori grape silver beet broccoli kombu beet greens fava bean potato quandong celery...</p>\r\n",
        "date": "August 24, 2009",
        "id": 1,
        "img_url": "https://images.unsplash.com/photo-1530482054429-cc491f61333b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1651&q=80",
        "subtitle": "Who knew that cacti lived such interesting lives.",
        "title": "The Life of Cacti"
    },
    {
        "author": "John Doe",
        "body": "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit...</p>",
        "date": "September 15, 2020",
        "id": 2,
        "img_url": "https://images.unsplash.com/photo-1601477410044-5861060cb66a?ixlib=rb-1.2.1&auto=format&fit=crop&w=1650&q=80",
        "subtitle": "Exploring the World of Coding",
        "title": "Coding Adventures"
    },
    {
        "author": "Jane Smith",
        "body": "<p>Quisque vehicula velit a mauris ullamcorper luctus...</p>",
        "date": "July 8, 2021",
        "id": 3,
        "img_url": "https://images.unsplash.com/photo-1629730471015-4b9817f066ec?ixlib=rb-1.2.1&auto=format&fit=crop&w=1650&q=80",
        "subtitle": "The Beauty of Nature",
        "title": "Nature's Wonders"
    }
];

// Insert multiple documents
db.blog.insertMany(documentsToInsert);