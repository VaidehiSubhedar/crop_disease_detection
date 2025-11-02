import pymongo

products = [
    {
        "name": "Organic Fertilizer",
        "price": 20,
        "image_url": "https://rukminim2.flixcart.com/image/850/1000/ku04o7k0/soil-manure/l/i/a/0-5-organic-potash-fertilizer-for-home-plants-gardening-purpose-original-imag77n8ph98vexd.jpeg?q=90&crop=false"
    },
    {
        "name": "Hybrid Maize Seeds",
        "price": 15,
        "image_url": "https://5.imimg.com/data5/SELLER/Default/2022/8/VD/XW/AS/57404107/sumo-plus-hybrid-maize-seeds.jpg"
    },
    {
        "name": "Wheat Seeds",
        "price": 12,
        "image_url": "https://5.imimg.com/data5/SELLER/Default/2023/12/366158440/JK/RT/VC/58096402/wheat.png"
    },
    {
        "name": "Potassium Nitrate Fertilizer",
        "price": 25,
        "image_url": "https://www.jiomart.com/images/product/original/rv3wpethis/gacil-white-potassium-nitrate-crystalline-fertilizer-powder-500-g-product-images-orv3wpethis-p599990345-0-202308161510.jpg?im=Resize=(420,420)"
    },
    {
        "name": "Hand Shovel",
        "price": 8,
        "image_url": "https://mlhobevaucyf.i.optimole.com/w:1200/h:742/q:mauto/f:best/ig:avif/https://newagri.in/wp-content/uploads/2023/06/AG018_Long_handle_shovel.jpg"
    },
    {
        "name": "Drip Irrigation Kit",
        "price": 50,
        "image_url": "https://m.media-amazon.com/images/I/71+488Q3p-L.jpg"
    },
    {
        "name": "Pesticide Spray Bottle",
        "price": 18,
        "image_url": "https://m.media-amazon.com/images/I/71RQEqyrZFL.jpg"
    },
    {
        "name": "Tractor Attachment - Plow",
        "price": 500,
        "image_url": "https://betstco.com/wp-content/uploads/2017/09/sp220--scaled.jpg"
    },
    {
        "name": "Compost Bin",
        "price": 30,
        "image_url": "https://mygreenbin.in/wp-content/uploads/2023/03/50-ltrs-Home-Composters.jpg"
    },
    {
        "name": "Cattle Feed",
        "price": 40,
        "image_url": "https://4.imimg.com/data4/SK/KL/ANDROID-1071315/product.jpeg"
    }
]


# Connection 
if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["NewDataBase"]
    products_collection = db["products"]  
    print("db is connected !")
    products_collection.insert_many(products)
    