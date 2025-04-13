from django.db import models

# Create your models here.
class PestDisease: 
    """
    Class to define structure for mango pests and diseases
    """
    def __init__(self, id, name, description, life_cycle, similar_to, damage, critical_control_period, monitoring, other_comments=None, image_url=None):
        self.id = id
        self.name = name 
        self.description = description
        self.life_cycle = life_cycle
        self.similar_to = similar_to
        self.damage = damage
        self.critical_control_period = critical_control_period
        self.monitoring = monitoring
        self.other_comments = other_comments
        self.image_url = image_url
        
    def __str__(self):
        return f"{self.name}" # returns representation of the object in string format 


# Creating instances of the pests info
def get_pests_diseases(): # This function returns a list of the information of all of the pests
    pests_diseases = [ 
        PestDisease(
            id=1,
            name="Longicorn beetle (Acalolepta mixtus, Family Cerambycidae)",
            description={
                "eggs": "Ovoid, white or light cream in colour.",
                "immatures": "Larvae are white or light cream with a brown head and constrictions along the length of the body. Size: Up to 40mm in length.",
                "adults": "Dark grey or brown with a mottled back and antennae that may be at least as long as the body. Size: 20-30mm in length."
            },
            life_cycle="One generation per year. Eggs are laid into cracks and crevices in branches or trunks that have been damaged. Larvae feed and tunnel under the bark or into the wood. Adults emerge from the trees after pupating in the tunnels.",
            similar_to="The damage is similar to that caused by auger beetles that produce smaller tunnels and finer sawdust.",
            damage="Recently pruned or stressed trees are more vulnerable to attack by longicorn. Affected trees have sap exudate on damaged areas and the bark may appear loose or lifted. Often damage is not noticed until the emergence holes of the adults are seen. Eventually the affected branches die.",
            critical_control_period="Late wet season and early dry season.",
            monitoring="Inspect trees for symptoms of stress or damage. Look for loose bark with lots of coarse sawdust underneath, for circular cut outs of bark with emergence holes underneath and holes packed with timber fibres. Symptoms are usually more obvious when they are advanced, especially during the dry season.",
            image_url="static/images/pest1.png"
        ),
        PestDisease(
            id=2,
            name="Mango seed weevil (Sternochetus mangiferae, Family Curculionidae)",
            description={
                "eggs": "Creamy white in colour and elongate. Size: 2mm in length.",
                "immatures": "White legless larva with a brown head.",
                "adults": "Dark brown to grey-black oval shaped weevil with a prominent snout. Mottled markings on wing covers. Size: 10mm in length."
            },
            life_cycle="Eggs are laid onto fruit that are about 30mm in length (or sometimes larger). After the egg is laid the weevil makes a small incision in the fruit skin which the sap flows out of and covers the egg gluing it to the surface of the fruit. After the larvae hatch they tunnel through the fruit flesh moving directly to the seed, this takes about 1-2 days. Larvae feed inside the seed until they pupate. The emergent adult chews through the hard seed coating within 2 months of fruit fall. Development from egg to adult takes approximately 53 days. There is only one generation per year.",
            similar_to="Other weevils.",
            damage="At egg laying, fruit may be covered in many spots of oozing sap. By the time fruit is harvested the egg laying scars noticeable. The only damage is to the seed.",
            critical_control_period="",
            monitoring="Adults may occasionally be seen moving onto branches and the outer canopy at flowering. Inspect young fruit for egg laying symptoms. Take random samples of fully developed fruit and cut fruit to inspect the seed for larvae or pupae.",
            other_comments="Mango seed weevil is a quarantine pest and fruit from infested properties should not be transported to uninfested areas. Removing fallen fruit reduces populations in infested areas. Pre-flowering and post-fruit set treatments of insecticide is recommended for control.",
            image_url="static/images/pest2.png"
        ),
        PestDisease(
            id=3,
            name="Red shouldered leaf beetle (Monolepta australis, Family Chrysomelidae)",
            description={
                "eggs": "Unknown (not normally seen as laid in soil).",
                "immatures": "White/cream in colour. Size: Up to 12mm in length (not normally seen).",
                "adults": "Yellow with a red spot on the base of each wing cover and a red mark across the top of the shoulders. Size: 4-8mm in length."
            },
            life_cycle="Eggs are laid into the soil. Larvae hatch in about 12 days and feed on the roots of grasses. They take about 3 months to mature. Larvae pupate in the soil, adult emergence takes place after the first rains at the onset of the wet season. There are usually two or three generations per year.",
            similar_to="A wide range of beetles.",
            damage="Leaves, flowers and fruit of native trees and horticultural tree crops may be affected. Large swarms of this beetle can cause defoliation, leaving behind a vein network (skeletonising), which dries out or turns brown. They can also strip the bark from small branches, which causes loss of vigour, poor fruit set and reduced fruit quality.",
            critical_control_period="Late wet season to flowering.",
            monitoring="Monitor new leaves in the early morning and evening, particularly during late wet season to flowering.",
            other_comments="Large swarms can develop between December and April. When conditions are optimal small numbers of beetles can survive throughout the dry season by sheltering under the leaves and bark of trees, especially in humid areas. Swarms generally occur in one or two trees on the outer edge of the orchard and within several hours or a few days may increase dramatically in numbers. They may occur in hot-spots and sometimes only a few trees on the edge of the orchard may be defoliated.",
            image_url="static/images/pest3.png"
        ),
        PestDisease(
            id=4,
            name="Swarming leaf beetles (Rhyparida spp., Geloptera aequalis, Family Chrysomelidae)",
            description={
                "eggs": "Unknown (not normally seen as laid in soil).",
                "immatures": "Larvae feed on grass roots and pupate in the soil (the larvae are not usually seen).",
                "adults": {
                    "Rhyparida": "Golden brown to black in colour with an oval shaped body. Size: 7-8mm in length.",
                    "Geloptera": "Glossy black with a metallic sheen. Size: 4-5mm in length."
                }
            },
            life_cycle="Adults emerge after the first rains at the onset of the wet season. Adults lay eggs into the soil. White larvae hatch from the eggs and feed on the roots of grasses until they are ready to pupate.",
            similar_to="A wide range of beetles.",
            damage="Adults prefer to feed on new leaves but may also damage bark. Large swarms may strip extensive patches of new growth causing significant leaf loss. Leaves will be completely eaten or they may be skelentonised and become brown and dried.",
            critical_control_period="November to March.",
            monitoring="Monitor new leaves in the early morning and evening, particularly during late wet season to flowering.",
            other_comments="Beetles may appear suddenly and in large numbers. May occur in hot spots on one or several trees rather than evenly spread throughout the orchard. They feed on a wide range of hosts.",
            image_url="static/images/pest4.png"
        ),
        PestDisease(
            id=5,
            name="Dimpling bug (Campylomma austrina, Family Miridae)",
            description={
                "eggs": "Unknown (not normally seen).",
                "immatures": "Nymphs are pale yellow and similar to adults but without wings.",
                "adults": "Oval, pale green to pale yellow and very active. Size: 2.5mm in length."
            },
            life_cycle="Eggs are laid onto flowers and developing fruit. Nymphs hatch and go through five instars before moulting into an adult. Development from egg to adult takes approximately 2 weeks.",
            similar_to="A variety of bugs in the same family.",
            damage="Adults and nymphs suck sap from flowers and developing fruit which initially causes slight pitting and pimpling, and may cause dimpling in the later stages of fruit development. Most of this damage grows out.",
            critical_control_period="Flowering and fruit set.",
            monitoring="To determine the presence of bugs, lightly tap the flower panicle onto a piece of paper and examine with a hand lens.",
            other_comments="Nymphs and adults are both sap feeders and predatory.",
            image_url="static/images/pest5.png"
        ),
        PestDisease(
            id=6,
            name="Fruitspotting bugs (Bananaspotting bug and Fruitspotting bug)",
            description={
                "scientific": "Amblypelta lutescens lutescens (Bananaspotting bug) and A. nitida (Fruitspotting bug) QLD only (Family Coreidae)",
                "eggs": "Pale green when first laid turning brown with a slight opalescence as they mature and oval in shape. Size: 2mm in length.",
                "immatures": "Nymphs have a black head with long antennae and a light green tear-drop shaped body with a red patch and two black dots surrounded with white circles. Fruitspotting bugs do not have the white circles.",
                "adults": "Light green with a light brown back (which includes the folded wings). Fruitspotting bug is usally darker green than bananaspotting bug. Size: 15mm in length."
            },
            life_cycle="Adult females lay a few single eggs each day onto young shoots and leaf petioles. They may lay more than 150 eggs in a life time. Once hatched the nymph goes through five instars before moulting into an adult. Development from egg to adult takes approximately 35-42. There may be 4-5 generations a year.",
            similar_to="Leaf and external fruit damage may appear similar to that of tea mosquito bug. Internal damage on mature fruit may be similar to stem end cavity disorder.",
            damage="Nymphs and adults suck sap from shoots and young fruit. When new pink shoots are attacked they wilt and die. Symptoms of attack in green shoots and young fruit are black marks where feeding has taken place. These marks later appear as elongate brown lesions which crack as the shoot or fruit expands during growth. Significant losses can occur during fruit set and early development. Newly set fruit turn brown and drop, older fruit can develop black, sunken marks or cracks. Mature fruit when cut can display a distinct cavity.",
            critical_control_period="Peak flushing periods during the late wet season and early dry season. Fruit development at all stages.",
            monitoring="Check young shoots for lesions at least once a week. Adults and nymphs are difficult to find.",
            image_url="static/images/pest6.png"
        ),
        PestDisease(
            id=7,
            name="Graptostethus bugs (Graptostethus spp., Family Lygaeidae)",
            description={
                "eggs": "Unknown (not normally seen).",
                "immatures": "Similar to adult but smaller and without wings (not normally seen).",
                "adults": "Orange-red with a 'cross' pattern made by the folded wings. Size: 7-9mm in length."
            },
            life_cycle="Development time from egg to adult is 45-81 days. Eggs take 14-21 days to hatch, nymphs develop in about 30 days, adults live for about 80 days.",
            similar_to="A variety of similarly coloured swarming bugs.",
            damage="May occur on flowers and shoots in very large numbers but they do not feed on fruit trees. Some scratch marks may be seen on trees affected by large swarms.",
            critical_control_period="Spray only if there is physical damage to flowers, scratching damage to fruit, or the likelihood of structural damage to branches.",
            monitoring="Look for swarms in flowers and on leaves.",
            other_comments="Four species are recorded from the Northern Territory. These bugs feed on seed pods of some field crops, native plants and weeds.",
            image_url="static/images/pest7.png"
        ),
    ]
    return pests_diseases