from pymongo import MongoClient
import os

FLAG = os.environ.get("FLAG", "wxmctf{dummy")
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost")

def db_init():
  client = MongoClient(MONGO_URI)

  db = client.store
  products = db.products
  products.delete_many({})

  hardware_list = [
    {
      "name": "CPU",
      "description": "Intel Core i7-10700K Processor",
      "price": 299.99,
      "stock": 10,
      "image_link": "https://www.gamestreet.lk/images/products/2533.jpg",
      "is_available": 1,
      "is_published": 1,
      "category": "hardware"
    },
    {
      "name": "GPU",
      "description": "NVIDIA GeForce RTX 3080",
      "price": 699.99,
      "stock": 5,
      "image_link": "https://imageio.forbes.com/specials-images/imageserve/5f615e7f718725a0a188f91c/NVIDIA-GeForce-RTX-3080-Graphics-Card-And-Box/960x0.jpg?format=jpg&width=960",
      "is_available": 1,
      "is_published": 1,
      "category": "hardware"
    },
    {
      "name": "RAM",
      "description": "Corsair Vengeance LPX 16GB (2 x 8GB) DDR4",
      "price": 99.99,
      "stock": 15,
      "image_link": "https://m.media-amazon.com/images/I/41a2jzudKtL._AC_UF894,1000_QL80_.jpg",
      "is_available": 1,
      "is_published": 1,
      "category": "hardware"
    },
    {
      "name": "Storage",
      "description": "Samsung 970 EVO Plus 1TB NVMe SSD",
      "price": 149.99,
      "stock": 8,
      "image_link": "https://www.gamestreet.lk/images/products/2066.jpg",
      "is_available": 1,
      "is_published": 1,
      "category": "hardware"
    },
    {
      "name": "Motherboard",
      "description": "ASUS ROG Strix Z590-E Gaming",
      "price": 349.99,
      "stock": 6,
      "image_link": "https://90a1c75758623581b3f8-5c119c3de181c9857fcb2784776b17ef.ssl.cf2.rackcdn.com/632960_225490_05_package_comping.jpg",
      "is_available": 1,
      "is_published": 0,
      "category": "hardware"
    }
  ]


  acc_list = [
    {
      "name": "Headphones",
      "description": "Wireless Noise-Canceling Headphones",
      "price": 149.99,
      "stock": 20,
      "image_link": "https://wish.lk/wp-content/uploads/2020/12/Sony-WH-1000XM4-Wireless-Noise-Canceling-Overhead-Headphones-1.jpg",
      "is_available": 1,
      "is_published": 1,
      "category": "accessory"
    },
    {
      "name": "Microphone",
      "description": "USB Condenser Microphone",
      "price": 79.99,
      "stock": 15,
      "image_link": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTrY9o0G4v99va4jdixateW-dTGsY1sn9L5Xw&usqp=CAU",
      "is_available": 1,
      "is_published": 1,
      "category": "accessory"
    },
    {
      "name": "Gaming Mouse",
      "description": "Wired RGB Gaming Mouse",
      "price": 39.99,
      "stock": 25,
      "image_link": "https://riocomputers.lk/store/image/cache/catalog/Component/Peripherals/Mouse/901541-MR44Mouse_30_315-800x800.webp",
      "is_available": 1,
      "is_published": 1,
      "category": "accessory"
    },
    {
      "name": "FLAG",
      "description": FLAG,
      "price": 69420.00,
      "stock": 1,
      "image_link": "https://i.etsystatic.com/36379723/r/il/29e8de/4673016317/il_1588xN.4673016317_hupm.jpg",
      "is_available": 1,
      "is_published": 0,
      "category": "accessory"
    }
  ]

  laptop_list = [
    {
      "name": "Dell XPS 13",
      "description": "13-inch Ultrabook with Intel Core i7",
      "price": 1399.99,
      "stock": 10,
      "image_link": "https://cdn.mos.cms.futurecdn.net/BDukEYkihdiTjmm9Wa6X3o.jpg",
      "is_available": 1,
      "is_published": 1,
      "category": "laptop"
    },
    {
      "name": "Apple MacBook Pro",
      "description": "16-inch Laptop with M1 Pro chip",
      "price": 2399.99,
      "stock": 5,
      "image_link": "https://iriver.lk/storage/macbook-pro-m2-14/mkgp3/20230513-002113-0000-540x600.jpg",
      "is_available": 1,
      "is_published": 1,
      "category": "laptop"
    },
    {
      "name": "HP Spectre x360",
      "description": "2-in-1 Convertible Laptop with OLED display",
      "price": 1299.99,
      "stock": 8,
      "image_link": "https://www.expertreviews.co.uk/sites/expertreviews/files/2022/03/best_2-in-1_laptop_lead.jpg",
      "is_available": 1,
      "is_published": 1,
      "category": "laptop"
    },
    {
      "name": "Lenovo ThinkPad X1 Carbon",
      "description": "14-inch Business Laptop with Intel Core i7",
      "price": 1599.99,
      "stock": 6,
      "image_link": "https://www.notebookcheck.net/fileadmin/Notebooks/News/_nc3/HP_Pavilion_Plus_14_inch_Laptop_PC_image_10.jpg",
      "is_available": 1,
      "is_published": 0,
      "category": "laptop"
    }
  ]


  products.insert_many(hardware_list)
  products.insert_many(acc_list)
  products.insert_many(laptop_list)

