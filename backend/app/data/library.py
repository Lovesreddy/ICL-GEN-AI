"""Curated knowledge articles, fertilizer guides, pest guides, and FAQs.

The wording is educational. It is not a local prescription or a certification ruling.
"""

DISCLAIMER = (
    "This is educational guidance drawn from widely described organic farming practice. "
    "Rates, varieties, and legal rules vary by soil, season, and country. Confirm important "
    "decisions with a local agriculture extension officer or your organic certifier."
)

KNOWLEDGE = [
    {
        "id": "soil-preparation",
        "title": "Soil preparation",
        "category": "soil",
        "summary": "Prepare a living soil before sowing: drainage, organic matter, and a seedbed matched to the crop.",
        "description": "Soil preparation in organic farming starts with the condition of the field rather than with a bag of fertilizer. The aim is a seedbed that roots can enter, that holds moisture without staying waterlogged, and that already contains decomposed organic matter. Walk the field after rain. Note where water stands, where the surface crusts, and where previous crops were weak. Those observations decide whether the first job is a drain, a bund, a load of compost, or simply timely ploughing.",
        "benefits": [
            "Better root growth and more even germination.",
            "Less erosion when residue and beds slow runoff.",
            "Higher water-holding capacity as organic matter increases.",
            "Fewer soil-borne problems when raw manure and waterlogging are avoided.",
        ],
        "steps": [
            "Clear plastic, stones, and diseased crop residue. Healthy straw may be composted or used as mulch rather than burned.",
            "Test soil when you can. Note texture, pH, and whether a hard pan stops roots. Extension laboratories can do a basic test.",
            "Plough or loosen only as deep as needed. Work soil when it is moist, not sticky and not dust-dry.",
            "Spread well-decomposed compost or farmyard manure and incorporate it in the top soil. Do not apply fresh dung against seed.",
            "Level fields for rice and make raised beds or ridges for vegetables, turmeric, and groundnut where drainage is poor.",
            "Form bunds on slopes, add a green-manure crop if the calendar allows, and prepare a fine but not powdery seedbed.",
        ],
        "materials": ["Compost or decomposed farmyard manure", "Green-manure seed where a window exists", "Field implements", "Soil-test report if available"],
        "examples": [
            "A tomato bed on sandy loam receives two to three centimetres of compost worked into the top 15 centimetres, then a straw mulch after transplanting.",
            "A rice field that crusts is puddled only after a dhaincha crop has been turned in, instead of relying on fertilizer at transplanting.",
        ],
        "related_crops": ["Rice", "Tomato", "Groundnut", "Turmeric"],
        "precautions": [
            "Working wet clay compacts the soil for the whole season.",
            "Deep ploughing on a steep slope without bunds increases erosion.",
            "Raw manure can burn seedlings and may carry weed seeds and pathogens.",
        ],
    },
    {
        "id": "organic-fertilizers",
        "title": "Organic fertilizers",
        "category": "fertilizer",
        "summary": "Feed the soil with decomposed organic materials, legumes, and carefully used biofertilizers.",
        "description": "Organic fertilizers are materials whose nutrients become available as soil organisms break them down. Compost, farmyard manure, vermicompost, green manure, oil cakes, and microbial inoculants each do a different job. Bulky manures improve structure and supply a broad, slow release of nutrients. Cakes and some biofertilizers are supplements. A common mistake is to treat a liquid preparation as if it could replace several tonnes of organic matter on a cereal or sugarcane crop.",
        "benefits": [
            "Organic matter improves infiltration and water holding.",
            "Nutrients are released over time, which suits long-season crops.",
            "Legumes and biofertilizers can add nitrogen when they match the crop.",
            "Soil life that cycles nutrients is fed along with the crop.",
        ],
        "steps": [
            "Identify the main limitation: low organic matter, poor nodulation, or a hungry previous crop.",
            "Apply bulky compost or manure at land preparation so it is in the root zone.",
            "Use a legume rotation or green manure where nitrogen is the main need.",
            "Add oil cake or vermicompost as a smaller, more concentrated dressing near high-value crops.",
            "Use biofertilizers as seed or soil treatments only when the product matches the crop, and follow the label.",
            "Record what was applied, the area, and the crop response so the next season is based on observation.",
        ],
        "materials": ["Compost", "Farmyard manure", "Vermicompost", "Neem cake or other oil cakes", "Green-manure seed", "A labelled biofertilizer if used"],
        "examples": [
            "Wheat after cowpea needs less added nitrogen than wheat after another cereal.",
            "Banana pits are filled with compost because the plant cannot wait for a thin dusting of cake alone.",
        ],
        "related_crops": ["Wheat", "Banana", "Sugarcane", "Tomato"],
        "precautions": [
            "Fresh poultry manure and fresh dung can scorch roots.",
            "Biofertilizers are living products. Heat, direct sun, and expired packets reduce their value.",
            "Certified farms must use only inputs allowed by their standard.",
        ],
    },
    {
        "id": "compost-preparation",
        "title": "Compost preparation",
        "category": "compost",
        "summary": "Turn crop waste and manure into a stable soil amendment with air, moisture, and time.",
        "description": "Compost is decomposed organic matter. A good pile mixes nitrogen-rich green materials with carbon-rich brown materials, stays about as moist as a wrung sponge, and is turned so air reaches the centre. Heat in an active pile kills many weed seeds and pathogens, but the edges stay cooler, so turning matters. Finished compost is dark, crumbly, and smells like forest soil, not ammonia or rot.",
        "benefits": [
            "Recycles on-farm waste.",
            "Improves soil structure and nutrient holding.",
            "Reduces the volume of residue and the viability of many weed seeds when the pile heats evenly.",
            "Gives a stable amendment that is safer for seedlings than fresh manure.",
        ],
        "steps": [
            "Choose a shaded, well-drained spot away from wells and kitchen doors.",
            "Chop bulky stalks so they wet through. Mix roughly two to three parts dry brown material with one part fresh green material or dung, by volume.",
            "Build the pile in layers about one to one and a half metres high. Sprinkle water so every layer is moist.",
            "Cover with straw, banana leaves, or a perforated sheet to limit drying and nutrient loss in heavy rain.",
            "Turn the pile after it heats, commonly after one to two weeks, and again two or three times. Move the outside material to the middle.",
            "Cure the compost until it no longer heats and plant roots would be safe in it. This often takes two to four months depending on the mix and the weather.",
        ],
        "materials": ["Crop residue and dry leaves", "Fresh weeds that have not set seed", "Dung if available", "Water", "A cover", "A fork for turning"],
        "examples": [
            "Rice straw mixed with cow dung and green weeds, turned three times, is a typical farm compost for the next nursery.",
            "A pile that smells of ammonia needs more dry leaves and a turning. A pile that is white and dusty needs water.",
        ],
        "related_crops": ["Rice", "Wheat", "Tomato", "Mango"],
        "precautions": [
            "Do not compost meat, plastic, treated wood, or pesticide-contaminated plants if the compost is for an organic field.",
            "Keep the pile out of floodwater so nutrients do not wash into a well or stream.",
            "A pile that never heats may still mature, but it will not kill weed seeds reliably.",
        ],
    },
    {
        "id": "vermicomposting",
        "title": "Vermicomposting",
        "category": "compost",
        "summary": "Earthworms convert pre-decomposed organic waste into castings that are useful as a concentrated soil amendment.",
        "description": "Vermicomposting uses surface-feeding worms, most often Eisenia fetida or a similar epigeic species, to consume partly decomposed organic matter. The castings are fine, dark, and rich in plant-available nutrients and microbial activity. Worms are not a substitute for a large compost programme on cereals, but they are valuable for nurseries, vegetables, and side-dressing. Worms need bedding, moderate moisture, and protection from heat, ants, and waterlogging. They do not thrive in a fresh, heating manure pile.",
        "benefits": [
            "Produces a fine amendment suited to nurseries and planting holes.",
            "Reduces kitchen and farm vegetable waste.",
            "Improves soil aggregation when used regularly.",
            "Can be made in small beds close to the homestead.",
        ],
        "steps": [
            "Build a bed, tank, or windrow in full shade with a floor that drains. A common farm bed is about one metre wide and 30 to 45 centimetres deep.",
            "Add moist bedding: decomposed dung, leaf compost, coconut coir, or shredded cardboard. The material should already have passed its hot stage.",
            "Introduce a known worm culture. A starting density often discussed in extension guides is several hundred adult worms per square metre, increased as the farmer gains experience.",
            "Feed in thin layers of chopped vegetable waste, pre-composted dung, and spent crop residues. Avoid meat, oil, citrus in large amounts, and fresh poultry manure.",
            "Keep the bed as moist as a wrung sponge. Cover it with wet sacking or leaves. Protect it from chickens, ants, rats, and direct sun.",
            "After about six to eight weeks, stop feeding a section so worms move toward fresh food, then harvest the finished castings. Dry them in shade and screen out remaining worms.",
        ],
        "materials": ["Epigeic earthworms", "Shade and a drained bed", "Pre-decomposed dung or compost", "Vegetable waste", "Water and a breathable cover"],
        "examples": [
            "A tomato grower mixes one or two handfuls of vermicompost into each planting hole and keeps the rest of the fertility in a basal compost dressing.",
            "A school garden feeds the worm bed with canteen vegetable peelings and uses the castings for potting mix, blended with soil and coarse compost.",
        ],
        "related_crops": ["Tomato", "Chilli", "Turmeric", "Banana"],
        "precautions": [
            "Hot, fresh dung will kill worms. Pre-compost it until it no longer heats.",
            "Too much water drives air out of the bed and the worms leave or die.",
            "Castings that heat up in a sealed bag were not finished. Dry and cure them in the shade.",
        ],
    },
    {
        "id": "natural-pest-management",
        "title": "Natural pest management",
        "category": "pest",
        "summary": "Prevent pests with healthy crops, monitoring, natural enemies, and botanical sprays used carefully.",
        "description": "Natural pest management begins before any spray is mixed. A vigorous plant on well-drained soil, a crop rotation, clean seed, and a field that still harbours spiders, wasps, and ladybirds will need fewer interventions. The farmer scouts on a fixed walk each week, identifies the actual insect, and acts when damage is rising rather than on a calendar. Botanical sprays such as neem oil are tools with limits. They can also harm beneficial insects and pollinators if they are used carelessly.",
        "benefits": [
            "Reduces dependence on synthetic pesticides.",
            "Protects pollinators and natural enemies when interventions are selective.",
            "Lowers the chance of residue problems at harvest.",
            "Builds farm knowledge through regular scouting records.",
        ],
        "steps": [
            "Prevent: use healthy seed, resistant varieties, rotation, balanced organic matter, and sanitation.",
            "Monitor: inspect leaves, stems, and the soil line. Record the pest, the crop stage, and the number of damaged plants.",
            "Identify natural enemies already present before you spray.",
            "Use physical and cultural methods first: hand removal, traps, mulch, trap crops, and destruction of badly infested residues.",
            "If a spray is justified, choose a product allowed by your organic standard, mix the recommended dilution, and spray in the evening.",
            "Return after a few days to see whether the treatment worked. Change the method if it did not, rather than simply spraying more often.",
        ],
        "materials": ["Hand lens or close observation", "Field notebook", "Yellow sticky traps", "Neem oil and mild soap where a spray is appropriate", "Gloves and eye protection"],
        "examples": [
            "Tomato fruit borer is reduced by picking damaged fruit every two days and by a marigold border, with neem used only if new damage continues.",
            "Rice leaf folders are watched first. A spray is considered only if damaged leaves increase across the field, not because a neighbour sprayed.",
        ],
        "related_crops": ["Rice", "Tomato", "Cotton", "Mango"],
        "precautions": [
            "Botanical pesticides are still pesticides. Keep them off skin, eyes, fish ponds, and open flowers.",
            "Spraying at noon in hot weather can scorch leaves.",
            "Misidentifying a beneficial insect as a pest leads to unnecessary sprays.",
        ],
    },
    {
        "id": "crop-rotation",
        "title": "Crop rotation",
        "category": "general",
        "summary": "Change crop families through the seasons so pests, diseases, and nutrient demand do not build up.",
        "description": "Crop rotation is a planned sequence of crops on the same land. A useful sequence changes plant family, rooting depth, and nutrient demand. Cereals often follow legumes. Solanaceous vegetables such as tomato and chilli should not follow each other. A restorative green manure or a break crop is part of the rotation, not an interruption of it. Writing the sequence down is what separates a rotation from a series of last-minute choices.",
        "benefits": [
            "Breaks the cycle of soil-borne diseases and some insects.",
            "Uses nutrients left by the previous crop.",
            "Improves soil structure when deep-rooted and fibrous-rooted crops alternate.",
            "Spreads labour and market risk across the year.",
        ],
        "steps": [
            "List the crops you can sell or eat and group them by family: cereals, legumes, solanaceae, cucurbits, alliums, and so on.",
            "Place a legume before the hungriest crop when seed and water allow.",
            "Avoid planting the same family in the same bed two seasons in a row.",
            "Include a green manure or a weeding fallow if disease or nutsedge has become severe.",
            "Match the sequence to rainfall. Do not plan an irrigated rabi crop you cannot water.",
            "Review the plan after harvest and note which pests actually appeared.",
        ],
        "materials": ["A seasonal calendar", "Seed for the next two crops", "Records from the previous season"],
        "examples": [
            "Cowpea or mung, then wheat, then a summer green manure is a simple cereal-legume pattern.",
            "Tomato followed by onion or a cereal is safer than tomato followed by chilli.",
        ],
        "related_crops": ["Wheat", "Tomato", "Chilli", "Groundnut"],
        "precautions": [
            "A rotation on paper fails if volunteer plants of the previous crop are left to host the same disease.",
            "Do not treat a legume as a complete fertilizer programme. It contributes nitrogen; it does not supply every nutrient.",
        ],
    },
    {
        "id": "intercropping",
        "title": "Intercropping",
        "category": "general",
        "summary": "Grow compatible crops together so light, roots, and ground cover are used more fully.",
        "description": "Intercropping places two or more crops in the same field at the same time. The combination works when the crops do not compete for the same space at the same moment. A tall cereal can protect a low legume. A fast crop can be harvested before a slow crop closes the canopy. Organic farmers also use intercrops and borders to confuse pests and to shelter natural enemies. Spacing must still leave room to weed and to harvest.",
        "benefits": [
            "More than one product from the same rainfall.",
            "Ground cover that shades weeds and protects soil.",
            "Sometimes fewer pests than in a large single-crop block.",
            "A legume intercrop can contribute nitrogen to the system.",
        ],
        "steps": [
            "Choose a main crop and a companion with a different height or duration.",
            "Set rows so the shorter crop still receives light. North-south rows are often easier to manage.",
            "Sow the companion at the same time or at the stage recommended locally so one crop does not smother the other.",
            "Weed early, because two crops make late weeding harder.",
            "Harvest the early crop carefully so you do not uproot the remaining one.",
            "Record the yield of both crops. An intercrop that ruins the main crop is not a success.",
        ],
        "materials": ["Seed of both crops", "A marked spacing plan", "Mulch if the soil dries quickly"],
        "examples": [
            "Groundnut with a row of pigeon pea uses the field after the groundnut is lifted.",
            "Turmeric grown in the light shade of young coconut or arecanut is a traditional multi-storey pattern in humid areas.",
            "Maize with cowpea covers the soil and supplies a pulse beside the cereal.",
        ],
        "related_crops": ["Groundnut", "Turmeric", "Cotton", "Sugarcane"],
        "precautions": [
            "Two hungry crops planted at full density will both yield poorly.",
            "Mixed harvests must be dried and stored separately so one wet crop does not spoil the other.",
        ],
    },
    {
        "id": "water-conservation",
        "title": "Water conservation",
        "category": "water",
        "summary": "Hold rain in the soil with mulch, organic matter, bunds, and irrigation that matches crop stage.",
        "description": "Water conservation on an organic farm is mostly soil management. Organic matter and mulch let rain enter and then slow its evaporation. Bunds, trenches, and a farm pond keep water on the land. Irrigation is timed to the stages when the crop actually forms yield, instead of keeping the surface wet every day. Rice can use alternate wetting and drying after establishment. Vegetables do better with drip or furrow water at the root than with a hose on the leaves.",
        "benefits": [
            "Longer gaps between irrigations on mulched soil.",
            "Less erosion and more groundwater recharge from slowed runoff.",
            "Fewer leaf diseases when foliage stays dry.",
            "Lower pumping cost.",
        ],
        "steps": [
            "Repair bunds and field channels before the monsoon.",
            "Add compost so the soil can hold what the rain delivers.",
            "Mulch wide-spaced crops as soon as the soil is moist.",
            "Level rice fields so a shallow water layer is even, and consider alternate wetting and drying after tillering if weeds are under control.",
            "Use drip or pitchers for orchards and vegetables where equipment or labour allows.",
            "Irrigate at the sensitive stages: crown-root initiation in wheat, flowering and boll fill in cotton, pegging in groundnut, fruit swell in tomato.",
        ],
        "materials": ["Mulch", "Compost", "Bunds or trenches", "Drip lines or watering cans", "A way to watch soil moisture"],
        "examples": [
            "Banana basins covered with chopped leaves need less frequent filling than bare basins in the same week.",
            "A groundnut field that is over-irrigated stays leafy and develops more leaf spot than a field watered at flowering and pod fill.",
        ],
        "related_crops": ["Rice", "Banana", "Groundnut", "Tomato"],
        "precautions": [
            "Alternate wetting and drying is not suitable for a field that already cracks and stresses the crop at flowering.",
            "Mulch against the stem of a seedling can keep the crown too wet.",
            "A farm pond needs a safe edge and should not receive runoff from a pesticide store or livestock yard.",
        ],
    },
    {
        "id": "organic-certification",
        "title": "Organic certification",
        "category": "certification",
        "summary": "Certification is a documented promise that the farm follows a named organic standard.",
        "description": "Organic certification is a third-party check against a written standard. In India the National Programme for Organic Production is the main framework for exported organic products, and other countries use their own rules, such as the USDA National Organic Program. The details differ. What is common is a transition period, a ban on synthetic fertilizers and synthetic pesticides, allowed-input lists, separation from conventional neighbours, and records. Selling a product as organic without the approval required in your market can be unlawful. This guide cannot certify a farm.",
        "benefits": [
            "Access to markets that pay for a verified organic claim.",
            "A written production standard instead of an informal definition.",
            "Regular inspection that catches drift, commingling, and incomplete records.",
            "A traceable lot from field to sale.",
        ],
        "steps": [
            "Choose the standard required by the buyer: domestic group certification, NPOP, or another national standard.",
            "Contact an accredited certification body or a local organic farmer group and ask for the current fee and the input list.",
            "Map fields, storage, and any conventional plots. Create buffer zones where spray drift is possible.",
            "Start records immediately: seed source, inputs, dates, harvest weights, and sales. Keep bills.",
            "Complete the transition period required by that standard. Crops grown during transition are usually not sold as organic.",
            "Host the inspection, close any non-compliances, and renew the certificate before it expires.",
        ],
        "materials": ["Field map", "Input purchase bills", "Seed labels", "Harvest and sales register", "The standard's allowed-input list"],
        "examples": [
            "A farm that uses one permitted biofertilizer and one unlisted fungicide can lose certification for that crop even if every other practice was organic.",
            "A grower group keeps one internal control file per member so the certifier can sample records instead of inventing them on inspection day.",
        ],
        "related_crops": ["Rice", "Cotton", "Turmeric", "Mango"],
        "precautions": [
            "Do not print an organic logo until the certifier authorises it.",
            "Borrowed spray equipment can contaminate an organic field.",
            "Standards change. Check the current list rather than a photocopy from several years ago.",
        ],
    },
    {
        "id": "sustainable-farming",
        "title": "Sustainable farming techniques",
        "category": "general",
        "summary": "Combine soil cover, diversity, careful water use, and records so the farm can keep producing.",
        "description": "Sustainable organic farming is a set of habits: keep the soil covered, keep living roots in the ground when possible, diversify crops, recycle nutrients, use water deliberately, and write down what happened. No single product creates a sustainable farm. The techniques on this site — compost, rotation, intercropping, mulch, and monitored pest control — work together. A farmer who adopts all of them in one week may fail from labour overload. A farmer who adds one practice each season and measures it will learn what fits the land.",
        "benefits": [
            "Yield that depends less on a single purchased input.",
            "Soil that is more resilient to a missed rain.",
            "Lower environmental load on streams and beneficial insects.",
            "Knowledge that stays on the farm when prices of inputs change.",
        ],
        "steps": [
            "Pick one weak point from last season: crusted soil, a repeated disease, or a water shortage.",
            "Choose one practice that addresses it and that you have the labour to finish.",
            "Apply it on part of the field if you are unsure, and leave a comparison strip.",
            "Record sowing date, inputs, rainfall or irrigations, pests, and yield.",
            "Keep what worked and drop what only added work.",
            "Share the result with neighbouring farmers and the extension officer, including the failures.",
        ],
        "materials": ["A notebook", "Seed and compost for the chosen practice", "A comparison area in the same field"],
        "examples": [
            "Mulching half a chilli field shows whether the water saving is worth the labour of gathering straw.",
            "A three-crop rotation written on the wall of the store is more useful than a long list of practices remembered only at sowing time.",
        ],
        "related_crops": ["Chilli", "Wheat", "Cotton", "Banana"],
        "precautions": [
            "Copying a practice from a wet district into a dry district without changing the variety or the spacing often fails.",
            "Sustainability claims on a label still require certification if the word organic is used for sale.",
        ],
    },
    {
        "id": "seed-selection-and-nursery",
        "title": "Seed selection and healthy nursery management",
        "category": "seeds",
        "summary": "Choose locally adapted, healthy seed and raise sturdy seedlings with clean water and good airflow.",
        "description": "A healthy crop begins with seed that suits the local season, soil, and market. Buy from a traceable source, check the variety and lot label, and avoid seed from diseased plants. For crops raised in nurseries, clean trays and a well-drained growing medium reduce damping-off. This guide gives general practices; use the local crop calendar for variety-specific timing.",
        "benefits": [
            "More even emergence and crop establishment.",
            "Fewer pests and diseases carried from the nursery into the field.",
            "Less seed and labour wasted on weak seedlings.",
        ],
        "steps": [
            "Select a variety recommended by a local agricultural extension service for the season and intended use.",
            "Check the seed label, lot, germination information, and any treatment instructions before opening the packet.",
            "For direct-sown crops, prepare a fine, moist seedbed and sow at the depth and spacing recommended for that crop.",
            "For nursery crops, clean trays and tools, use a porous seedling medium, and keep containers raised off contaminated soil.",
            "Water gently so the medium stays moist but not saturated; provide light and airflow as seedlings emerge.",
            "Remove weak or diseased seedlings and gradually expose sturdy seedlings to outdoor conditions before transplanting.",
            "Transplant during a cool part of the day, water in, and protect seedlings from harsh sun or wind while they establish.",
        ],
        "materials": ["Locally adapted seed", "Clean trays or a prepared seedbed", "Well-drained growing medium", "Clean water"],
        "examples": [
            "Tomato and brinjal are commonly raised in a nursery and transplanted when sturdy.",
            "Maize and okra are commonly sown directly when soil is warm and moist.",
        ],
        "related_crops": ["Tomato", "Brinjal", "Cabbage", "Maize", "Okra"],
        "precautions": [
            "Do not reuse nursery trays without cleaning them.",
            "Do not sow seed into waterlogged or cold soil unless the crop is suited to those conditions.",
            "Follow the seed label and local regulations for any seed treatment; do not eat treated seed.",
        ],
    },
    {
        "id": "mulching-and-weed-management",
        "title": "Mulching and practical weed management",
        "category": "soil",
        "summary": "Use clean soil cover and timely weed removal to conserve moisture and reduce competition.",
        "description": "Mulch protects the soil surface from sun and heavy rain, while early weed control prevents young weeds from competing with the crop. Mulch material, thickness, and timing must fit the crop and local pest pressure. Weed management is most effective when several small actions are planned before weeds set seed.",
        "benefits": [
            "Slower moisture loss and less soil splash onto leaves.",
            "Reduced erosion and more stable soil temperature.",
            "Fewer weeds when mulch is clean and applied at the right stage.",
        ],
        "steps": [
            "Remove established weeds before they set seed and keep perennial weeds from spreading by rhizomes or roots.",
            "Use clean, dry plant residue that has not been treated with persistent herbicides or contaminated materials.",
            "Apply mulch after the soil is moist and the crop is established, leaving an open ring around stems and trunks.",
            "Use shallow cultivation near crop roots and hand-weed close to plants to avoid root damage.",
            "Inspect under the mulch for slugs, rodents, or disease and adjust the material or depth if problems appear.",
            "Add crop rotation, cover crops, and timely planting to reduce the next flush of weeds.",
        ],
        "materials": ["Clean straw or leaf residue", "Hand hoe or suitable weeding tool", "Cover-crop seed where appropriate"],
        "examples": [
            "A vegetable bed can be mulched after seedlings are established and the soil has been watered.",
            "A cereal-legume rotation can interrupt weed cycles that build up under repeated monocropping.",
        ],
        "related_crops": ["Tomato", "Chilli", "Banana", "Groundnut", "Turmeric"],
        "precautions": [
            "Do not place wet mulch against stems; trapped moisture can encourage rot.",
            "Avoid spreading weed seed heads or diseased crop residue as mulch.",
            "Some crops need a bare planting strip for warming or emergence; check local recommendations.",
        ],
    },
    {
        "id": "soil-testing-and-nutrient-planning",
        "title": "Soil testing and organic nutrient planning",
        "category": "soil",
        "summary": "Use a representative soil test and crop history to choose amendments instead of guessing.",
        "description": "A soil test is a starting point for nutrient decisions, not a complete diagnosis of crop health. Samples must represent the field, and results should be interpreted with the crop, yield goal, irrigation water, and organic-standard requirements in mind. Compost and rotations build soil condition over time, while a test helps identify constraints that may need specific attention.",
        "benefits": [
            "Fewer unnecessary amendments and lower input costs.",
            "Earlier detection of pH, salinity, or nutrient constraints.",
            "A repeatable record for comparing fields and seasons.",
        ],
        "steps": [
            "Divide land into sampling areas with similar soil, slope, crop history, and management.",
            "Collect a representative sample from each area using the laboratory's clean tools, depth, and sampling instructions.",
            "Label samples clearly and tell the laboratory which crop is planned and whether the field is irrigated.",
            "Review the report with a qualified local adviser; do not treat a single result as a diagnosis of a leaf symptom.",
            "Prioritize mature compost, cover crops, and rotation, then add only amendments that are permitted and supported by the report.",
            "Keep the test, input receipts, application dates, and crop response together; retest at an interval advised by the laboratory.",
        ],
        "materials": ["Clean sampling tool", "Field map or notes", "Laboratory sample bags", "Recent crop and amendment history"],
        "examples": [
            "Separate a low-lying field from a well-drained field rather than mixing both into one sample.",
            "Compare soil-test trends over multiple seasons before changing a long-term nutrient plan.",
        ],
        "related_crops": ["Rice", "Wheat", "Tomato", "Groundnut", "Cotton"],
        "precautions": [
            "Do not sample immediately after applying an amendment unless the laboratory specifically advises it.",
            "Do not apply lime, gypsum, or micronutrients based only on a photograph or a generic online schedule.",
            "Check that every input is allowed by the farm's certification standard before application.",
        ],
    },
    {
        "id": "soil-types-india",
        "title": "Major soil groups in India",
        "category": "soil",
        "summary": "Recognize India's eight broad soil groups and understand why field testing still matters.",
        "description": (
            "The types of soils in India are commonly described using eight broad groups. "
            "Alluvial soils occur across the northern plains and river deltas; their texture and fertility vary, "
            "and rice, wheat, sugarcane, or jute may suit different locations. "
            "Black (regur) soils are clay-rich, hold water, and swell when wet and crack as they dry; cotton, "
            "sorghum, soybean, and pulses are grown in suitable areas. "
            "Red and yellow soils occur widely across the eastern and southern plateau; many are relatively low "
            "in organic matter, so millets, pulses, or groundnut depend on rainfall and soil management. "
            "Laterite soils form in strongly leached, high-rainfall regions; tea, coffee, and cashew are grown "
            "in some areas with suitable management. "
            "Arid soils are common in dry western regions and are often sandy with low organic matter; "
            "millets and pulses depend on local rainfall and available water. "
            "Forest and mountain soils vary with slope and elevation; horticulture and tea are grown in suitable "
            "locations, while steep or shallow soils need erosion protection. "
            "Saline and alkaline soils contain excess soluble salts or sodium that can restrict crops; "
            "testing and drainage assessment are needed before choosing reclamation steps. "
            "Peaty and marshy soils have high organic matter and often remain wet; rice and other wetland crops "
            "are grown where local water conditions allow. "
            "These are broad regional groups, not a diagnosis of an individual field."
        ),
        "benefits": [
            "Broad soil groups help compare landscapes and plan what to test.",
            "Understanding texture, drainage, and salinity helps avoid crop choices that do not fit field conditions.",
        ],
        "steps": [
            "Use the broad group as a starting clue, not as a substitute for observing the field.",
            "Check texture, drainage, pH, salinity, and organic matter through an appropriate soil test.",
            "Choose crops using the field result together with rainfall, irrigation water, season, and local extension advice.",
        ],
        "materials": ["Field history and location notes", "Representative soil sample", "Soil laboratory report when available"],
        "examples": [
            "A black clay soil may hold water well but require careful drainage and timing of field operations.",
            "A sandy arid soil may need water-conserving management, but irrigation water quality should also be checked.",
        ],
        "related_crops": ["Rice", "Wheat", "Cotton", "Groundnut", "Tea"],
        "precautions": [
            "Do not identify a field solely by soil color or a regional map.",
            "Do not apply gypsum, lime, or other amendments for salinity or sodicity without a soil test and local advice.",
            "Crop suitability varies within each group; check field conditions and local recommendations.",
        ],
    },
]

FERTILIZERS = [
    {
        "id": "vermicompost",
        "title": "Vermicompost",
        "category": "fertilizer",
        "summary": "Worm castings used as a fine organic amendment for beds, nurseries, and side-dressing.",
        "description": "Vermicompost is the stable material harvested from a worm bed. It is darker and finer than ordinary compost and is usually applied in smaller quantities because it is more concentrated and more work to produce. It improves seedling mixes and planting holes. It does not, by itself, meet the nutrient removal of a high-yielding sugarcane or rice crop.",
        "benefits": ["Fine texture for nurseries", "Steady nutrient release", "Improves soil aggregation", "Useful side-dressing for vegetables"],
        "steps": [
            "Produce castings as described in the vermicomposting guide, and cure them in the shade until they no longer heat.",
            "For vegetables, mix a modest amount into the bed or planting hole along with a larger basal dressing of compost.",
            "For nurseries, blend castings with soil and coarse compost rather than sowing into pure castings.",
            "Side-dress around established plants and cover with mulch so the material stays moist and is not blown away.",
        ],
        "materials": ["Finished vermicompost", "Basal compost", "Mulch"],
        "examples": ["Tomato and chilli planting holes", "Potting mix for mango and other tree nurseries"],
        "related_crops": ["Tomato", "Chilli", "Turmeric"],
        "precautions": ["Do not use unfinished, heating material against seed.", "Store castings in the shade with some air, not in a sealed wet sack."],
        "calculator_key": "vermicompost",
    },
    {
        "id": "farmyard-manure",
        "title": "Farmyard manure",
        "category": "fertilizer",
        "summary": "Decomposed livestock dung and bedding used as the main bulky organic manure.",
        "description": "Farmyard manure is a mixture of dung, urine-soaked bedding, and leftover fodder that has been heaped until it decomposes. Well-rotted manure is dark and does not smell strongly of ammonia. It is the backbone of fertility on many mixed organic farms. Fresh manure from the shed is not the same product.",
        "benefits": ["Adds organic matter in bulk", "Supplies a broad range of nutrients slowly", "Improves water holding on sandy soil", "Recycles livestock waste"],
        "steps": [
            "Heap manure under shade, keep it moist, and turn it until it is no longer hot or fibrous.",
            "Spread it before the final tillage so it sits in the root zone.",
            "On trees, spread it under the drip line and keep it off the bark.",
            "Follow it with mulch or incorporation the same day in hot sun so nitrogen is not lost from the surface.",
        ],
        "materials": ["Decomposed farmyard manure", "Transport and a fork", "Mulch or soil cover"],
        "examples": ["Basal manure for rice before puddling", "Annual ring application for mango"],
        "related_crops": ["Rice", "Wheat", "Mango", "Sugarcane"],
        "precautions": ["Fresh manure burns seedlings and can introduce weed seeds.", "Do not pile manure where rain washes it straight into a well or pond."],
        "calculator_key": "farmyard_manure",
    },
    {
        "id": "green-manure",
        "title": "Green manure",
        "category": "fertilizer",
        "summary": "A crop grown to be cut and turned into the soil while it is still green.",
        "description": "Green manures such as dhaincha, sunn hemp, and cowpea are grown for six to eight weeks and incorporated before they become woody. Leguminous green manures add nitrogen if they nodulate. They also add fresh organic matter and shade out some weeds. The following crop benefits only if the green manure is turned in with enough time and moisture to decompose.",
        "benefits": ["Adds nitrogen when a legume nodulates", "Protects bare soil", "Suppresses some weeds", "Improves the next seedbed"],
        "steps": [
            "Sow a locally adapted green-manure seed into moist soil after the previous harvest or just before the monsoon.",
            "Let it grow until flowering begins. Older, woody plants decompose slowly.",
            "Cut and incorporate it into moist soil, commonly two to three weeks before sowing or transplanting the main crop.",
            "If the window is short, compost the cut biomass instead of burying a large fresh mass against seed.",
        ],
        "materials": ["Green-manure seed", "Moisture for decomposition", "A way to cut and incorporate the crop"],
        "examples": ["Dhaincha before rice", "Cowpea before wheat where irrigation allows a short summer crop"],
        "related_crops": ["Rice", "Wheat", "Sugarcane"],
        "precautions": ["A thick layer of fresh green matter can temporarily tie up nitrogen and produce gases in waterlogged soil.", "Buy seed that is not contaminated with parasitic weeds."],
        "calculator_key": "green_manure",
    },
    {
        "id": "jeevamrutham",
        "title": "Jeevamrutham",
        "category": "fertilizer",
        "summary": "A traditional fermented microbial preparation used as a soil drench in Indian natural farming.",
        "description": "Jeevamrutham, also spelled jeevamrutha, is a fermented preparation associated with Subhash Palekar's Natural Farming. A commonly published farm recipe uses cow dung, cow urine, jaggery, pulse flour, a handful of uncontaminated living soil, and water, fermented for a few days in the shade and stirred. Farmers apply the liquid to soil to encourage microbial activity. Published recipes differ, and the preparation is not a measured chemical fertilizer. It works best where the soil already has organic matter and crop residue for microbes to feed on.",
        "benefits": ["Low-cost inoculant made on the farm", "Encourages biological activity when soil has residue to feed on", "Uses materials available on a mixed farm", "Can be applied through irrigation water"],
        "steps": [
            "Mix about 10 kilograms of fresh cow dung, 5 to 10 litres of cow urine, 1 to 2 kilograms of jaggery, 1 to 2 kilograms of pulse flour, and a handful of soil from an untreated field into about 200 litres of water. Recipes vary; treat these figures as a widely circulated traditional proportion, not a unique standard.",
            "Keep the drum in the shade. Stir clockwise and anticlockwise morning and evening.",
            "Use it after about two to five days, when it has fermented but before it smells putrid. Do not store it for weeks.",
            "Apply to moist soil, often along rows or with irrigation, at a traditional rate of about 200 litres per acre. Increase organic residues if the soil is bare and sandy.",
        ],
        "materials": ["Cow dung", "Cow urine", "Jaggery", "Pulse flour", "Living soil", "A 200-litre drum and clean water"],
        "examples": ["Soil drench for millets, cotton, and vegetables in natural-farming systems", "Used alongside mulch, not instead of all organic matter"],
        "related_crops": ["Cotton", "Tomato", "Chilli", "Groundnut"],
        "precautions": ["Use dung and urine only from animals that fit your certification rule.", "Do not drink the preparation.", "It does not replace bulky manure on a nutrient-hungry crop such as banana or sugarcane.", "If the drum smells rotten rather than fermented, discard it away from drinking water."],
        "calculator_key": "jeevamrutham",
    },
    {
        "id": "panchagavya",
        "title": "Panchagavya",
        "category": "fertilizer",
        "summary": "A traditional fermented blend of cow-derived ingredients used as a diluted foliar spray.",
        "description": "Panchagavya is a traditional preparation built from cow dung, cow urine, milk, curd, and ghee, often with jaggery, banana, and tender coconut water in farm recipes. It is fermented for about two to three weeks and then diluted before spraying. Farmers use it as a growth promoter. Evidence and recipes vary. It should be filtered and diluted, and it should not be sprayed on open flowers when bees are working.",
        "benefits": ["Uses on-farm ingredients", "Applied as a dilute foliar spray", "Some farmers report greener growth when the crop is otherwise well fed", "Can be prepared in a covered clay or plastic drum"],
        "steps": [
            "Follow a recipe from your extension service or certifier. A widely circulated version ferments dung and ghee first, then adds urine, milk, curd, and other ingredients over several days.",
            "Stir daily and keep the vessel shaded and covered with a cloth so gases can escape.",
            "After fermentation, filter the liquid. A commonly used spray dilution is about 3 percent, or 30 millilitres per litre of water. Confirm the dilution you were taught.",
            "Spray in the evening, on a healthy crop, and wash equipment afterwards.",
        ],
        "materials": ["Cow dung, urine, milk, curd, and ghee", "Jaggery and fruit if the chosen recipe includes them", "A fermenting vessel", "A sprayer and clean water"],
        "examples": ["Monthly foliar spray on vegetables during active growth", "Used on some fruit crops before flowering, stopped while bees are dense in the blossom"],
        "related_crops": ["Tomato", "Mango", "Banana", "Chilli"],
        "precautions": ["The liquid has a strong smell and can spoil if stored carelessly.", "Test a few plants before spraying a whole field in hot weather.", "Certified organic farms must check that every ingredient is allowed.", "Keep the concentrate away from children and drinking-water pots."],
        "calculator_key": "panchagavya",
    },
    {
        "id": "neem-cake",
        "title": "Neem cake",
        "category": "fertilizer",
        "summary": "The residue left after neem oil extraction, used as a soil amendment with some pest-suppressing effect.",
        "description": "Neem cake is the solid left after oil is pressed from neem seed. It contains plant nutrients and azadirachtin-related compounds that can discourage some soil insects and nematodes when mixed into soil. It is an amendment, not a stand-alone fertilizer. Quality varies with how the oil was extracted. Use cake that is free of adulterants and allowed by your organic standard.",
        "benefits": ["Adds organic nitrogen slowly", "Traditional soil amendment against some soil pests", "Useful in vegetable beds and spice crops", "Stores well when kept dry"],
        "steps": [
            "Buy cake from a known mill and keep it dry.",
            "Crush lumps and mix the cake into the soil or the planting row at land preparation. A commonly cited educational rate is about 200 kilograms per acre, adjusted for crop and soil.",
            "Do not place a thick dry layer in direct contact with germinating seed.",
            "Combine it with compost. Cake alone does not rebuild soil structure.",
        ],
        "materials": ["Neem cake", "Compost", "Gloves"],
        "examples": ["Mixed into turmeric beds", "A small amount in tomato planting holes together with compost"],
        "related_crops": ["Turmeric", "Tomato", "Chilli", "Banana"],
        "precautions": ["Dust irritates eyes and lungs. Wear a cloth and gloves.", "Do not dump surplus cake into ponds; neem compounds can affect aquatic life.", "Adulterated cake may contain materials forbidden in organic systems."],
        "calculator_key": "neem_cake",
    },
    {
        "id": "compost",
        "title": "Compost",
        "category": "fertilizer",
        "summary": "Fully decomposed mixed organic waste used as the general-purpose soil amendment.",
        "description": "Finished compost is the default organic fertilizer on this farm guide. Apply it where roots will grow, in amounts the farm can actually produce or buy. Vegetables and orchards usually show the benefit first. Cereals need larger volumes, which is why green manure and rotation sit beside the compost heap in a practical plan.",
        "benefits": ["Broad soil improvement", "Safer for seed than fresh waste", "Recycles residues", "Supports later use of microbial drenches"],
        "steps": [
            "Use only finished compost that is dark, cool, and crumbly.",
            "Spread and incorporate it during land preparation.",
            "On perennial crops, apply under the canopy and mulch over it.",
            "Keep records of how many cartloads went to each field.",
        ],
        "materials": ["Finished compost"],
        "examples": ["Basal dressing for wheat", "Pit mixture for banana"],
        "related_crops": ["Wheat", "Banana", "Rice", "Sugarcane"],
        "precautions": ["Unfinished compost can rob nitrogen and carry weed seeds.", "Compost made from sprayed crop waste can contaminate an organic field."],
        "calculator_key": "compost",
    },
    {
        "id": "biofertilizers",
        "title": "Biofertilizers",
        "category": "fertilizer",
        "summary": "Living inoculants such as Rhizobium, Azospirillum, and phosphate-solubilizing bacteria.",
        "description": "Biofertilizers are products that contain selected living microorganisms. Rhizobium helps specific legumes nodulate. Azospirillum and Azotobacter are used with some cereals and vegetables. Phosphate-solubilizing bacteria are intended to help plants use phosphorus already in the soil. They are not magic powders. The correct strain, a live packet, moist soil, and a matching crop all matter. Read the label for the crop and the expiry date.",
        "benefits": ["Supports nitrogen fixation in legumes when the strain matches", "Low application quantity", "Can improve use of existing soil nutrients", "Fits organic systems when the formulation is allowed"],
        "steps": [
            "Buy a packet labelled for your crop and check the expiry date and storage instructions.",
            "Mix seed treatment with a sticker such as jaggery solution or the method printed on the packet. Keep the seed out of direct sun.",
            "Sow into moist soil the same day when the label says to.",
            "For legume crops, do not expect nodulation if the seed was treated with a forbidden fungicide or if the soil is extremely dry.",
        ],
        "materials": ["The correct biofertilizer packet", "Clean water", "A shaded mixing place"],
        "examples": ["Rhizobium on groundnut", "Azotobacter on wheat", "Phosphate-solubilizing bacteria with compost in a vegetable bed"],
        "related_crops": ["Groundnut", "Wheat", "Sugarcane"],
        "precautions": ["A packet left on a hot dashboard is no longer a live inoculant.", "Do not mix with chemical fungicides unless the manufacturer explicitly allows that combination.", "Use the strain specified for the crop. A soybean Rhizobium is not the right choice for every legume."],
        "calculator_key": "biofertilizers",
    },
]

PESTS = [
    {
        "id": "neem-oil-spray",
        "title": "Neem oil spray",
        "category": "pest",
        "summary": "A botanical spray used against sucking pests and some young caterpillars.",
        "description": "Neem oil, pressed from neem seed, is used as a contact and antifeedant spray. A commonly taught educational dilution for field crops is about 5 millilitres of neem oil per litre of water, plus a few drops of a mild liquid soap so the oil mixes. Some products are already formulated and must be diluted exactly as their label says. Neem is most useful on aphids, whiteflies, and small caterpillars. It will not rescue a field of fully grown borers inside fruit.",
        "benefits": ["Widely available botanical option", "Useful against several sucking pests", "Breaks down in sunlight, so timing matters", "Can be part of an organic input list when the product is approved"],
        "steps": [
            "Confirm the product is allowed by your certifier if the crop is certified.",
            "Mix about 5 millilitres of pure neem oil and about 1 millilitre of mild soap in a small volume of water, then make up to 1 litre. Shake often. If you use a commercial formulation, ignore this household dilution and follow its label.",
            "Test the spray on a few leaves and wait a day, especially on tender seedlings and in hot weather.",
            "Spray in the evening, covering the underside of leaves. Keep people, animals, and bees out of the drift.",
            "Repeat only if monitoring shows the pest is still increasing. More frequent spraying is not automatically better.",
        ],
        "materials": ["Neem oil or a labelled neem formulation", "Mild soap as an emulsifier if required", "Clean water", "A sprayer", "Gloves and eye protection"],
        "examples": ["Aphids on chilli", "Whiteflies on tomato", "Early leaf-feeding caterpillars on vegetables"],
        "related_crops": ["Tomato", "Chilli", "Cotton", "Wheat"],
        "precautions": ["Oil and soap can burn leaves in strong sun.", "Neem is toxic to some aquatic organisms. Do not wash the sprayer into a pond.", "Protect eyes. Concentrated oil irritates skin.", "Do not spray open blossoms while pollinators are foraging."],
    },
    {
        "id": "biological-control",
        "title": "Biological pest control",
        "category": "pest",
        "summary": "Conserve or release living natural enemies, and use permitted microbial products when needed.",
        "description": "Biological control uses predators, parasitoids, and disease organisms of pests. Many are already in the field: ladybird beetles, spiders, lacewings, dragonflies, and tiny parasitic wasps. The first task is to stop killing them with broad sprays. The second is to give them nectar, unsprayed refuge, and time. Deliberate releases, such as Trichogramma wasps against moth eggs or a Bacillus thuringiensis product against caterpillars, are additional tools where a local supplier and an approved product exist.",
        "benefits": ["Works with the insects already on the farm", "Can be highly specific", "Reduces the need for sprays", "Supports pollination when refuges flower"],
        "steps": [
            "Learn to recognise at least five natural enemies on your crops.",
            "Keep a flowering border such as coriander, marigold, or native weeds that are not a harvest problem.",
            "Scout before any spray so you know whether predators are already increasing.",
            "If you release Trichogramma or a similar insect, follow the supplier's timing for the pest's egg stage. A late release does nothing.",
            "Use Bacillus thuringiensis only as a labelled product permitted by your organic standard, aimed at young caterpillars, and stored cool.",
        ],
        "materials": ["A scouting notebook", "Flowering refuge plants", "A reputable biocontrol supplier when releases are planned"],
        "examples": ["Ladybirds feeding on aphids in wheat", "Trichogramma releases timed to bollworm eggs in cotton", "Bt products against young tomato fruit worm where the certifier allows them"],
        "related_crops": ["Cotton", "Tomato", "Rice", "Wheat"],
        "precautions": ["A biocontrol insect released into a field that is sprayed the next day is wasted money.", "Microbial products have expiry dates and temperature limits.", "Not every wasp or beetle is beneficial. Identify before you act."],
    },
    {
        "id": "companion-planting",
        "title": "Companion planting",
        "category": "pest",
        "summary": "Place mutually useful plants together to confuse pests, attract natural enemies, or use space better.",
        "description": "Companion planting is a form of intercropping chosen for pest and soil effects as well as yield. Evidence is stronger for some pairs than for others. Marigold with tomato is widely used because the flower can reduce some nematode pressure and it attracts beneficial insects. Basil and onion are traditional companions in kitchen gardens. Companion planting does not make a crop immune. It is one layer beside sanitation, soil health, and monitoring.",
        "benefits": ["Adds diversity in a small space", "Can support natural enemies with nectar and shelter", "Some combinations suppress specific soil pests", "Gives a second harvest"],
        "steps": [
            "Pick a companion that you will actually use or sell.",
            "Give both plants enough light and root space. A companion sown too thick becomes a weed.",
            "Use marigold as a border or inter-row in solanaceous crops rather than as a complete control method.",
            "Observe whether pest damage is lower than in a nearby single-crop bed. Keep the comparison honest.",
        ],
        "materials": ["Companion seed", "A spacing plan"],
        "examples": ["Marigold around tomato", "Onion near carrot in a garden bed", "Coriander left to flower beside vegetables as a wasp nectar source"],
        "related_crops": ["Tomato", "Chilli", "Cotton"],
        "precautions": ["A companion from the same disease family can make the problem worse.", "Do not rely on companion planting alone for a serious outbreak."],
    },
    {
        "id": "trap-crops",
        "title": "Trap crops",
        "category": "pest",
        "summary": "A preferred plant, sown as a border or strip, draws pests away from the main crop so they can be destroyed there.",
        "description": "A trap crop is more attractive to a pest than the crop you want to protect. Pests gather on the trap and can be removed by cutting, crushing, or a targeted spray, while the main crop is left alone. The trap must be planted early enough to be attractive at the right time, and it must be destroyed before the pests multiply and move back. An unmanaged trap crop becomes a nursery.",
        "benefits": ["Concentrates pests in a small area", "Reduces spraying of the main crop", "Makes scouting faster", "Can be combined with biological control"],
        "steps": [
            "Learn which local trap works for your pest. Examples used in extension programmes include marigold or a designated border for some cotton and vegetable pests, and mustard as a trap for some pests of cabbage-family crops.",
            "Sow the trap earlier or at the spacing that makes it more attractive than the main crop.",
            "Inspect the trap twice a week.",
            "Destroy the infested trap plants before the next generation of the pest emerges. Removing them late is worse than not planting them.",
        ],
        "materials": ["Trap-crop seed", "Labour for timely destruction", "A scouting routine"],
        "examples": ["A marigold or okra border watched for bollworm eggs beside cotton", "Mustard rows in a cabbage-family garden, pulled and buried when they are heavily infested"],
        "related_crops": ["Cotton", "Tomato", "Chilli"],
        "precautions": ["A forgotten trap crop increases the pest.", "Do not put the trap on the downwind side only and then ignore the rest of the border.", "Confirm the local pest-trap pairing with extension staff. Attractiveness is regional."],
    },
    {
        "id": "botanical-pesticides",
        "title": "Botanical pesticides",
        "category": "pest",
        "summary": "Plant-based sprays such as neem, garlic-chilli extract, and other traditional preparations.",
        "description": "Botanical pesticides are made from plants. Neem is the best known. Farmers also ferment or soak garlic and chilli, or use other local plants recommended by extension. These preparations can irritate skin and eyes, and some are toxic to fish and to beneficial insects. A traditional origin does not make a spray harmless. Use gloves, filter the liquid, and apply the weakest dilution that has worked in your own small test.",
        "benefits": ["Ingredients may be available on the farm or in the local market", "Usually break down faster than many synthetic pesticides", "Useful for small sucking-pest colonies", "Fit some organic standards when the recipe is allowed"],
        "steps": [
            "Choose a recipe your certifier and extension office accept. A simple garlic-chilli extract uses a handful of garlic and a few ripe chillies crushed in water, left overnight, filtered, and heavily diluted.",
            "Add a drop of soap if the spray must spread on waxy leaves.",
            "Strain it so sprayer nozzles do not clog.",
            "Spray a test patch, wear protection, and apply in the evening.",
            "Record the dilution. If it scorched the test patch, do not spray the field.",
        ],
        "materials": ["Neem, garlic, or chilli", "Clean water", "Soap if needed", "Filter cloth", "Gloves and eye protection"],
        "examples": ["A dilute garlic-chilli spray for aphids on a garden crop", "Neem oil for whiteflies when a soap emulsifier is used"],
        "related_crops": ["Chilli", "Tomato", "Wheat"],
        "precautions": ["Chilli and garlic extracts burn eyes and broken skin.", "Keep all botanical concentrates away from children and labelled as sprays, not as food.", "Do not use tobacco extracts. Nicotine preparations are highly toxic and are not an acceptable organic practice in this guide.", "Never spray near a fish pond or a drinking-water source."],
    },
    {
        "id": "integrated-pest-management",
        "title": "Integrated pest management",
        "category": "pest",
        "summary": "A decision process that combines prevention, monitoring, and the least disruptive control that still protects the crop.",
        "description": "Integrated pest management, or IPM, is a way of deciding. It fits organic farming when every control you choose is allowed by the organic standard. The sequence is prevention, observation, identification, threshold, and only then a control. Cultural methods come before biological methods, and biological methods come before botanical sprays. Calendar spraying, where a product is applied every week regardless of what is on the plant, is the habit IPM is meant to replace.",
        "benefits": ["Fewer unnecessary sprays", "Better use of natural enemies", "Decisions you can explain to a certifier", "Records that improve next season"],
        "steps": [
            "Prevent problems with variety, rotation, healthy seedlings, and field sanitation.",
            "Scout on the same weekday. Look at a set number of plants, not only the damaged ones near the path.",
            "Identify the pest and note whether natural enemies are present.",
            "Act when damage or pest numbers cross a level you have agreed with extension guidance, not when you first see a single insect.",
            "Choose the least disruptive allowed method and check afterwards whether it worked.",
            "Write down the date, the pest, the action, and the result.",
        ],
        "materials": ["Scouting plan", "Identification help from extension", "Allowed inputs", "A notebook"],
        "examples": ["Rice: perching sticks and water management before any spray against leaf feeders", "Cotton: weekly square inspection and a trap crop before a neem or Bt application"],
        "related_crops": ["Rice", "Cotton", "Tomato", "Mango"],
        "precautions": ["IPM is not a product you can buy. A bottle labelled IPM is still just one tool.", "Thresholds from another region may not match your variety and climate.", "An organic farm cannot adopt the chemical step of a conventional IPM leaflet."],
    },
]

FAQS = [
    {"id": 1, "category": "Soil", "question": "How can I improve soil fertility naturally?", "answer": "Add finished compost or decomposed farmyard manure, keep the soil covered with mulch or a living crop, and rotate with a legume or green manure. Test the soil if crops stay poor after organic matter has increased. Avoid burning residue and avoid working the soil when it is very wet."},
    {"id": 2, "category": "Soil", "question": "Which crops are suitable for sandy soil?", "answer": "Groundnut, watermelon-type cucurbits, and some millets tolerate sandy soil better than rice or banana. Sandy loam can also support tomato, chilli, and turmeric if you add compost and mulch so water and nutrients do not wash through. Sandy soil is a poor choice for crops that need standing water."},
    {"id": 3, "category": "Fertilizers", "question": "How can I prepare organic fertilizer for tomato plants?", "answer": "Work finished compost or farmyard manure into the bed before transplanting, add a small amount of vermicompost or neem cake in the planting hole, and mulch after the seedlings are established. Side-dress with compost at flowering. A microbial drench such as jeevamrutham can supplement this, but it does not replace the bulky compost."},
    {"id": 4, "category": "Fertilizers", "question": "What is the process of vermicomposting?", "answer": "Place epigeic worms such as Eisenia fetida in a shaded, drained bed of pre-decomposed dung or compost. Feed thin layers of vegetable waste and keep the bedding as moist as a wrung sponge. Avoid meat, oil, and fresh hot manure. Harvest castings after about six to eight weeks from a section you have stopped feeding."},
    {"id": 5, "category": "Pests", "question": "Which organic pesticides are suitable for rice crops?", "answer": "Start with resistant varieties, clean seedlings, removal of grassy weed hosts, and conservation of spiders and dragonflies. Neem oil can be used against some leaf-feeding insects when monitoring shows they are increasing. A Bacillus thuringiensis product may be used for caterpillars if your organic standard allows that specific product. Identify the insect before spraying."},
    {"id": 6, "category": "Pests", "question": "How can I control pests without chemical pesticides?", "answer": "Use healthy seed, rotation, scouting, hand removal, traps, trap crops, and natural enemies. Botanical sprays such as neem are a later step, used in the evening and kept away from bees and ponds. This is integrated pest management limited to organic methods."},
    {"id": 7, "category": "Water", "question": "How often should I irrigate organic vegetables?", "answer": "Water when the root zone begins to dry, not on a fixed daily schedule. Mulch lengthens the interval. Tomato and chilli need steady moisture from flowering to fruit swell. Wet the soil at the base rather than the leaves, and water in the morning or with drip so plants do not stay wet overnight."},
    {"id": 8, "category": "Certification", "question": "How long does organic certification take?", "answer": "Most standards require a transition period, often two to three years, before a crop can be sold as organic. The exact period depends on the standard and on what was applied to the land before. Contact an accredited certifier for the rule that applies to your market."},
    {"id": 9, "category": "Crops", "question": "Can I grow tomato and chilli in the same bed every year?", "answer": "It is better not to. They belong to the same family and share wilt, blight, and several pests. Rotate with a crop from another family, such as a cereal, a legume, or an onion crop, and remove volunteer plants."},
    {"id": 10, "category": "Fertilizers", "question": "Is fresh cow dung good for seedlings?", "answer": "No. Fresh dung heats, releases ammonia, and can carry weed seeds and pathogens. Compost or vermicompost it first. Well-rotted farmyard manure can be mixed into a nursery bed, but it should not be the entire medium."},
    {"id": 11, "category": "Pests", "question": "When should I spray neem oil?", "answer": "Spray in the evening after you have confirmed a sucking pest or a young caterpillar, and after a test on a few leaves. A commonly taught dilution is about 5 millilitres of neem oil per litre of water with a little soap, unless the product label gives a different rate. Do not spray open flowers while bees are foraging."},
    {"id": 12, "category": "Soil", "question": "What does a good compost pile need?", "answer": "A mixture of green and dry materials, moisture like a wrung sponge, and air from turning. A pile about one metre across can heat. Finished compost is dark, crumbly, and does not smell of ammonia. Keep plastic and diseased, sprayed plants out of an organic pile."},
]


def render_article(article: dict) -> str:
    lines = [
        f"Title: {article['title']}",
        f"Category: {article['category']}",
        f"Source: {article.get('source', 'Organic Farming Guide educational knowledge base')}",
        "",
        article["description"],
        "",
        "Benefits:",
    ]
    lines.extend(f"- {item}" for item in article["benefits"])
    lines.append("")
    lines.append("Step-by-step instructions:")
    lines.extend(f"{index}. {step}" for index, step in enumerate(article["steps"], start=1))
    lines.append("")
    lines.append("Required materials:")
    lines.extend(f"- {item}" for item in article["materials"])
    lines.append("")
    lines.append("Practical examples:")
    lines.extend(f"- {item}" for item in article["examples"])
    lines.append("")
    lines.append("Related crops: " + ", ".join(article["related_crops"]))
    if article.get("precautions"):
        lines.append("")
        lines.append("Precautions:")
        lines.extend(f"- {item}" for item in article["precautions"])
    lines.append("")
    lines.append(DISCLAIMER)
    return "\n".join(lines)


def render_crop(crop: dict) -> str:
    lines = [
        f"Title: {crop['crop_name']} organic cultivation guide",
        "Category: crop",
        "Source: Organic Farming Guide educational knowledge base",
        "",
        crop["description"],
        "",
        f"Suitable soil: {crop['suitable_soil']}",
        f"Climate: {crop['climate']}",
        f"Sowing season: {crop['sowing_season']}",
        f"Water need: {crop['water_need']}",
        "",
        f"Organic fertilizers: {crop['organic_fertilizers']}",
        "",
        f"Irrigation: {crop['irrigation']}",
        "",
        f"Natural pest management: {crop['pest_management']}",
        "",
        f"Harvesting: {crop['harvesting']}",
        "",
        DISCLAIMER,
    ]
    return "\n".join(lines)
