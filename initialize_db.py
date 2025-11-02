import pymongo

# IMPORTANT: Replace this with your MongoDB Atlas connection string
# Example: "mongodb+srv://<username>:<password>@<cluster-url>/<database-name>?retryWrites=true&w=majority"
MONGO_ATLAS_CONNECTION_STRING = "YOUR_MONGODB_ATLAS_CONNECTION_STRING" 

disease_management =[
  {
    "disease": "Apple___Apple_scab",
    "prevention": [
      "Plant resistant apple varieties.",
      "Prune trees to improve air circulation.",
      "Remove and destroy fallen leaves and infected fruit to reduce fungal spores.",
      "Apply appropriate fungicides during the growing season."
    ],
    "remedies": [
      "Apply fungicides such as captan or sulfur before infection periods.",
      "Implement cultural practices like proper pruning and sanitation to reduce disease incidence."
    ]
  },
  {
    "disease": "Apple___Black_rot",
    "prevention": [
      "Remove and destroy mummified fruit and pruned branches.",
      "Ensure proper spacing and pruning to improve air circulation.",
      "Apply appropriate fungicides during the growing season."
    ],
    "remedies": [
      "Use fungicides like captan or sulfur during bloom and pre-harvest periods.",
      "Practice regular orchard sanitation to minimize infection sources."
    ]
  },
  {
    "disease": "Apple___Cedar_apple_rust",
    "prevention": [
      "Avoid planting apple trees near Eastern red cedar or juniper species.",
      "Remove galls from nearby cedar or juniper trees before they produce spores.",
      "Choose rust-resistant apple varieties when planting new trees."
    ],
    "remedies": [
      "Apply fungicides containing fenarimol or myclobutanil during the growing season.",
      "Monitor and manage nearby cedar or juniper trees to reduce spore production."
    ]
  },
  {
    "disease": "Apple___healthy",
    "prevention": [
      "Keep monitoring the crop and ensure optimal conditions for growth."
    ],
    "remedies": [
      "Maintain good orchard practices."
    ]
  },
  {
    "disease": "Blueberry___healthy",
    "prevention": [
      "Maintain good irrigation and nutrient levels."
    ],
    "remedies": [
      "Ensure proper soil management and care."
    ]
  },
  {
    "disease": "Cherry_(including_sour)___Powdery_mildew",
    "prevention": [
      "Ensure proper air circulation around the plants."
    ],
    "remedies": [
      "Prune affected parts and apply a sulfur-based fungicide."
    ]
  },
  {
    "disease": "Cherry_(including_sour)___healthy",
    "prevention": [
      "Regularly inspect for any early signs of disease and maintain optimal conditions."
    ],
    "remedies": [
      "Maintain good orchard practices."
    ]
  },
  {
    "disease": "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "prevention": [
      "Practice crop rotation and use resistant varieties."
    ],
    "remedies": [
      "Apply fungicides with active ingredients like azoxystrobin or pyraclostrobin."
    ]
  },
  {
    "disease": "Corn_(maize)___Common_rust_",
    "prevention": [
      "Plant rust-resistant corn hybrids.",
      "Avoid late planting dates which can increase disease severity.",
      "Manage irrigation to reduce humidity levels around plants."
    ],
    "remedies": [
      "Apply fungicides if the disease appears early and weather conditions favor its development.",
      "Monitor fields regularly to detect and manage initial infections promptly."
    ]
  },
  {
    "disease": "Corn_(maize)___Northern_Leaf_Blight",
    "prevention": [
      "Use resistant corn hybrids.",
      "Rotate crops with non-host species to reduce inoculum levels.",
      "Manage crop residues through tillage to decrease pathogen survival."
    ],
    "remedies": [
      "Apply fungicides when disease risk is high and prior to tasseling.",
      "Ensure balanced fertilization to promote robust plant health."
    ]
  },
  {
    "disease": "Corn_(maize)___healthy",
    "prevention": [
      "Use of resistant/tolerant hybrids.",
      "Crop rotation with a non host crop like legumes.",
      "Destruction of crop debris."
    ],
    "remedies": [
      "Foliar spray of recommended fungicides immediately after symptoms appearance.",
      "Repeat sprays at recommended intervals if needed."
    ]
  },
  {
    "disease": "Grape___Black_rot",
    "prevention": [
      "Remove and destroy mummified berries and diseased canes.",
      "Ensure proper canopy management to improve air circulation.",
      "Apply appropriate fungicides during the growing season."
    ],
    "remedies": [
      "Use fungicides at critical growth stages, such as when new shoots are 10 inches long.",
      "Implement cultural practices like pruning and sanitation to reduce disease incidence."
    ]
  },
  {
    "disease": "Grape___Esca_(Black_Measles)",
    "prevention": [
      "Avoid wounding vines during pruning and other vineyard operations.",
      "Remove and destroy infected wood and vines.",
      "Manage irrigation to prevent water stress."
    ],
    "remedies": [
      "There are no effective chemical treatments; focus on preventive cultural practices.",
      "Replant with certified disease-free stock if vineyard infection is severe."
    ]
  },
  {
    "disease": "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "prevention": [
      "Implement proper canopy management to reduce humidity and leaf wetness.",
      "Remove and destroy infected leaves and pruning debris.",
      "Apply appropriate fungicides during the growing season."
    ],
    "remedies": [
      "Use fungicides effective against leaf spot diseases at recommended intervals.",
      "Maintain vineyard sanitation to minimize disease spread."
    ]
  },
  {
    "disease": "Grape___healthy",
    "prevention": [
      "Maintain good vineyard management practices."
    ],
    "remedies": [
      "Ensure proper care and monitoring of the vines."
    ]
  },
  {
    "disease": "Orange___Haunglongbing_(Citrus_greening)",
    "prevention": [
      "Use disease-free planting material.",
      "Control the Asian citrus psyllid vector through insecticides and biological agents.",
      "Remove and destroy infected trees to reduce disease spread."
    ],
    "remedies": [
      "There is no cure; focus on vector control and removal of infected trees.",
      "Implement nutritional therapies to prolong productivity of mildly affected trees."
    ]
  },
  {
    "disease": "Peach___Bacterial_spot",
    "prevention": [
      "Plant resistant peach varieties.",
      "Avoid overhead irrigation to reduce leaf wetness.",
      "Apply copper-based bactericides during the growing season."
    ],
    "remedies": [
      "Use bactericides like copper compounds at labeled rates and timings.",
      "Implement cultural practices to reduce tree stress and susceptibility."
    ]
  },
  {
    "disease": "Peach___healthy",
    "prevention": [
      "Maintain good orchard management practices."
    ],
    "remedies": [
      "Ensure proper care and monitoring of the trees."
    ]
  },
  {
    "disease": "Pepper,_bell___Bacterial_spot",
    "prevention": [
      "Plant-certified, disease-free seeds.",
      "Use resistant varieties if available in your area.",
      "Inspect fields regularly for signs of the disease.",
      "Remove and burn any seedling or plants with leaf spots, as well as adjacent plants.",
      "Remove weeds in and around the field.",
      "Plan a 2-3 year crop rotation with non-susceptible plants.",
      "Mulch around plants to avoid soil to plant contamination.",
      "Clean tools and equipment after use.",
      "Avoid overhead irrigation and working in fields when foliage is wet.",
      "Plow plant debris deep into the soil after harvest or remove and burn them.",
      "Ensure adequate plant spacing for better air circulation.",
      "Regularly prune plants to remove excess foliage and improve air flow.",
      "Use organic mulches to reduce soil splash and maintain soil moisture levels.",
      "Incorporate organic matter into the soil to enhance its structure and microbial diversity."
    ],
    "remedies": [
      "Copper-containing bactericides can be used as a protectant and give partial disease control.",
      "Apply bactericides at the first sign of disease and then at 10- to 14-day intervals when warm, moist conditions prevail.",
      "The active ingredients copper and mancozeb give better protection.",
      "Consider destroying the entire crop if the disease occurs early in the season.",
      "Bacterial viruses (bacteriophages) that specifically kill the bacteria are available.",
      "Submerge seeds for one minute in 1.3% sodium hypochlorite or in hot water (50°C) for 25 minutes.",
      "Implement Integrated Pest Management (IPM) combining cultural, biological, and chemical controls."
    ]
  },
  {
    "disease": "Pepper,_bell___healthy",
    "prevention": [
      "Maintain good agricultural practices."
    ],
    "remedies": [
      "Ensure proper care and monitoring of the plants."
    ]
  },
  {
    "disease": "Potato___Early_blight",
    "prevention": [
      "Rotate crops to prevent pathogen buildup.",
      "Stake plants to improve air circulation.",
      "Water at the base to keep foliage dry."
    ],
    "remedies": [
      "Apply fungicides containing chlorothalonil or copper-based compounds.",
      "Remove and destroy infected plant debris to reduce inoculum."
    ]
  },
  {
    "disease": "Potato___Late_blight",
    "prevention": [
      "Use certified disease-free seeds and transplants.",
      "Avoid overhead irrigation to minimize leaf wetness.",
      "Apply appropriate fungicides preventatively during favorable conditions."
    ],
    "remedies": [
      "Use fungicides like chlorothalonil or copper-based products at the first sign of disease.",
      "Remove and destroy infected plants immediately to prevent spread."
    ]
  },
  {
    "disease": "Potato___healthy",
    "prevention": [
      "Plant late blight-free seed tubers.",
      "Do not mix seed lots because cutting can transmit late blight.",
      "Use a seed piece fungicide treatment labeled for control of late blight.",
      "Avoid planting problem areas that may remain wet for extended periods.",
      "Avoid excessive and/or nighttime irrigation.",
      "Eliminate sources of inoculum such as hairy nightshade weed species and volunteer potatoes."
    ],
    "remedies": [
      "Scout fields regularly.",
      "Use foliar fungicides on a regular and continuing schedule once late blight is present.",
      "Quickly destroy hot spots of late blight.",
      "Kill vines completely two to three weeks before harvest, considering a fungicide at vine killing if there is late blight pressure.",
      "Applying phosphorous acid to potatoes after harvest and before piling can prevent infection and the spread of late blight in storage.",
      "Monitor home garden and market tomatoes near you for late blight."
    ]
  },
  {
    "disease": "Raspberry___healthy",
    "prevention": [
      "Ensure good practices such as proper pruning and support."
    ],
    "remedies": [
      "Maintain healthy growing conditions."
    ]
  },
  {
    "disease": "Soybean___healthy",
    "prevention": [
      "Maintain good agricultural practices."
    ],
    "remedies": [
      "Ensure proper care and monitoring of the plants."
    ]
  },
  {
    "disease": "Squash___Powdery_mildew",
    "prevention": [
      "Plant resistant varieties.",
      "Ensure good air circulation by proper spacing and pruning.",
      "Avoid excessive nitrogen fertilization."
    ],
    "remedies": [
      "Apply fungicides such as sulfur or potassium bicarbonate at the first sign of infection.",
      "Remove and destroy infected leaves."
    ]
  },
  {
    "disease": "Strawberry___Leaf_scorch",
    "prevention": [
      "Plant resistant varieties.",
      "Ensure good air circulation.",
      "Avoid excessive moisture on leaves."
    ],
    "remedies": [
      "Apply appropriate fungicides.",
      "Remove and destroy infected leaves."
    ]
  },
  {
    "disease": "Strawberry___healthy",
    "prevention": [
      "Maintain good agricultural practices."
    ],
    "remedies": [
      "Ensure proper care and monitoring of the plants."
    ]
  },
  {
    "disease": "Tomato___Bacterial_spot",
    "prevention": [
      "Plant resistant tomato varieties.",
      "Avoid overhead irrigation.",
      "Practice crop rotation.",
      "Ensure good air circulation through proper spacing and pruning."
    ],
    "remedies": [
      "Apply copper-based bactericides at the first sign of infection.",
      "Remove and destroy infected leaves and plant parts.",
      "Use certified disease-free seeds and transplants."
    ]
  },
  {
    "disease": "Tomato___Early_blight",
    "prevention": [
      "Rotate crops to prevent pathogen buildup.",
      "Stake plants to improve air circulation.",
      "Water at the base to keep foliage dry."
    ],
    "remedies": [
      "Apply fungicides containing chlorothalonil or copper-based compounds.",
      "Remove and destroy infected plant debris to reduce inoculum."
    ]
  },
  {
    "disease": "Tomato___Late_blight",
    "prevention": [
      "Use certified disease-free seeds and transplants.",
      "Avoid overhead irrigation to minimize leaf wetness.",
      "Apply appropriate fungicides preventatively during favorable conditions."
    ],
    "remedies": [
      "Use fungicides like chlorothalonil or copper-based products at the first sign of disease.",
      "Remove and destroy infected plants immediately to prevent spread."
    ]
  },
  {
    "disease": "Tomato___Leaf_Mold",
    "prevention": [
      "Ensure proper spacing between plants to promote air circulation.",
      "Avoid overhead watering; use drip irrigation to keep foliage dry.",
      "Maintain greenhouse humidity below 85% to inhibit fungal growth.",
      "Remove and destroy infected plant debris to reduce inoculum sources.",
      "Sanitize greenhouses between crop cycles to eliminate residual spores."
    ],
    "remedies": [
      "Apply fungicides containing chlorothalonil or copper formulations at the first sign of infection.",
      "Implement cultural practices like pruning and staking to improve ventilation."
    ]
  },
  {
    "disease": "Tomato___Septoria_leaf_spot",
    "prevention": [
      "Rotate crops annually to prevent pathogen buildup in the soil.",
      "Stake and mulch plants to reduce soil splash and improve air circulation.",
      "Water at the base of the plant to keep leaves dry and minimize fungal spread.",
      "Remove and destroy infected leaves promptly to prevent disease progression."
    ],
    "remedies": [
      "Apply fungicides such as chlorothalonil or copper-based products at the onset of symptoms.",
      "Use organic options like neem oil to control the spread of the disease."
    ]
  },
  {
    "disease": "Tomato___Spider_mites Two-spotted_spider_mite",
    "prevention": [
      "Maintain adequate plant hydration, as water-stressed plants are more susceptible.",
      "Encourage natural predators like ladybugs and predatory mites in the garden.",
      "Avoid excessive nitrogen fertilization, which can promote mite populations."
    ],
    "remedies": [
      "Spray plants with water to dislodge mites and reduce their numbers.",
      "Apply insecticidal soaps or horticultural oils to affected areas, ensuring thorough coverage.",
      "Introduce biological controls such as predatory mites to manage infestations."
    ]
  },
  {
    "disease": "Tomato___Target_Spot",
    "prevention": [
      "Implement crop rotation to reduce pathogen presence in the soil.",
      "Ensure proper plant spacing and pruning to enhance air circulation.",
      "Avoid overhead irrigation to minimize leaf wetness."
    ],
    "remedies": [
      "Apply appropriate fungicides when conditions favor disease development.",
      "Remove and destroy infected plant material to reduce inoculum sources."
    ]
  },
  {
    "disease": "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "prevention": [
      "Plant resistant tomato varieties.",
      "Control whitefly populations, the primary vector of the virus, using insecticides or reflective mulches.",
      "Remove and destroy infected plants promptly to prevent disease spread.",
      "Maintain weed-free fields to reduce alternative hosts for the virus."
    ],
    "remedies": [
      "There is no effective treatment for infected plants; focus on preventive measures.",
      "Implement integrated pest management strategies to control whitefly populations."
    ]
  },
  {
    "disease": "Tomato___Tomato_mosaic_virus",
    "prevention": [
      "Use certified disease-free seeds and transplants.",
      "Practice good sanitation by disinfecting tools and washing hands after handling tobacco products.",
      "Remove and destroy infected plants to prevent the spread of the virus."
    ],
    "remedies": [
      "There is no cure for infected plants; emphasize preventive practices.",
      "Control aphid populations, which can transmit the virus, through appropriate insecticides."
    ]
  }
]
  
if __name__ == "__main__":
    try:
        client = pymongo.MongoClient(MONGO_ATLAS_CONNECTION_STRING)
        db = client["NewDataBase"] 
        collection = db['SampleCollection']
        print("Database connected:", db.name)
        
        # Optional: Clear existing data before inserting if you want a fresh start
        collection.delete_many({})
        
        collection.insert_many(disease_management)
        print("Data uploaded successfully to MongoDB Atlas!")
    except pymongo.errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB Atlas: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")