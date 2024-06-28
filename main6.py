import os
import firebase_admin
from firebase_admin import credentials, storage, db
from fpdf import FPDF
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from email.mime.text import MIMEText
import smtplib
import random
from dateutil import parser
import string
from datetime import datetime
import requests
import hashlib
import fitz  # PyMuPDF
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image, ImageOps
import pytesseract
from sentence_transformers import SentenceTransformer, util
import numpy as np

os.environ["TOKENIZERS_PARALLELISM"] = "false"
cred = credentials.Certificate('/Users/LakshSarda/Downloads/csia-acb9d-firebase-adminsdk-3rgsb-e4a48f992c.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://csia-acb9d-default-rtdb.firebaseio.com',
    'storageBucket': 'csia-acb9d.appspot.com'
})
syllabus_details = [
    ["1 States of matter",
        ["1.1 Solids, liquids and gases",
            ["1 State the distinguishing properties of solids, liquids and gases",
            "2 Describe the structures of solids, liquids and gases in terms of particle separation, arrangement and motion",
            "3 Describe changes of state in terms of melting, boiling, evaporating, freezing and condensing",
            "4 Describe the effects of temperature and pressure on the volume of a gas",
            "5 Explain changes of state in terms of kinetic particle theory, including the interpretation of heating and cooling curves",
            "6 Explain, in terms of kinetic particle theory, the effects of temperature and pressure on the volume of a gas"]
        ],
        ["1.2 Diffusion",
            ["1 Describe and explain diffusion in terms of kinetic particle theory",
            "2 Describe and explain the effect of relative molecular mass on the rate of diffusion of gases"]
        ]
    ],
    ["2 Atoms, elements and compounds",
        ["2.1 Elements, compounds and mixtures",
            ["1 Describe the differences between elements, compounds and mixtures"]
        ],
        ["2.2 Atomic structure and the Periodic Table",
            ["1 Describe the structure of the atom as a central nucleus containing neutrons and protons surrounded by electrons in shells",
            "2 State the relative charges and relative masses of a proton, a neutron and an electron",
            "3 Define proton number / atomic number as the number of protons in the nucleus of an atom",
            "4 Define mass number / nucleon number as the total number of protons and neutrons in the nucleus of an atom",
            "5 Determine the electronic configuration of elements and their ions with proton number 1 to 20, e.g. 2,8,3",
            "6 State that: (a) Group VIII noble gases have a full outer shell (b) the number of outer shell electrons is equal to the group number in Groups I to VII (c) the number of occupied electron shells is equal to the period number"]
        ],
        ["2.3 Isotopes",
            ["1 Define isotopes as different atoms of the same element that have the same number of protons but different numbers of neutrons",
            "2 Interpret and use symbols for atoms, e.g. 12C6, and ions, e.g. 35Cl17−",
            "3 State that isotopes of the same element have the same chemical properties because they have the same number of electrons and therefore the same electronic configuration",
            "4 Calculate the relative atomic mass of an element from the relative masses and abundances of its isotopes"]
        ],
        ["2.4 Ions and ionic bonds",
            ["1 Describe the formation of positive ions, known as cations, and negative ions, known as anions",
            "2 State that an ionic bond is a strong electrostatic attraction between oppositely charged ions",
            "3 Describe the formation of ionic bonds between elements from Group I and Group VII, including the use of dot-and-cross diagrams",
            "4 Describe the properties of ionic compounds: (a) high melting points and boiling points (b) good electrical conductivity when aqueous or molten and poor when solid",
            "5 Describe the giant lattice structure of ionic compounds as a regular arrangement of alternating positive and negative ions",
            "6 Describe the formation of ionic bonds between ions of metallic and non-metallic elements, including the use of dot-and-cross diagrams",
            "7 Explain in terms of structure and bonding the properties of ionic compounds: (a) high melting points and boiling points (b) good electrical conductivity when aqueous or molten and poor when solid"]
        ],
        ["2.5 Simple molecules and covalent bonds",
            ["1 State that a covalent bond is formed when a pair of electrons is shared between two atoms leading to noble gas electronic configurations",
            "2 Describe the formation of covalent bonds in simple molecules, including H2, Cl2, H2O, CH4, NH3 and HCl. Use dot-and-cross diagrams to show the electronic configurations in these and similar molecules",
            "3 Describe in terms of structure and bonding the properties of simple molecular compounds: (a) low melting points and boiling points (b) poor electrical conductivity",
            "4 Describe the formation of covalent bonds in simple molecules, including CH3OH, C2H4, O2, CO2 and N2. Use dot-and-cross diagrams to show the electronic configurations in these and similar molecules",
            "5 Explain in terms of structure and bonding the properties of simple molecular compounds: (a) low melting points and boiling points in terms of weak intermolecular forces (specific types of intermolecular forces are not required) (b) poor electrical conductivity"]
        ],
        ["2.6 Giant covalent structures",
            ["1 Describe the giant covalent structures of graphite and diamond",
            "2 Relate the structures and bonding of graphite and diamond to their uses, limited to: (a) graphite as a lubricant and as an electrode (b) diamond in cutting tools",
            "3 Describe the giant covalent structure of silicon(IV) oxide, SiO2",
            "4 Describe the similarity in properties between diamond and silicon(IV) oxide, related to their structures"]
        ],
        ["2.7 Metallic bonding",
            ["1 Describe metallic bonding as the electrostatic attraction between the positive ions in a giant metallic lattice and a ‘sea’ of delocalised electrons",
            "2 Explain in terms of structure and bonding the properties of metals: (a) good electrical conductivity (b) malleability and ductility"]
        ]
    ],
    ["3 Stoichiometry",
        ["3.1 Formulae",
            ["1 State the formulae of the elements and compounds named in the subject content",
            "2 Define the molecular formula of a compound as the number and type of different atoms in one molecule",
            "3 Deduce the formula of a simple compound from the relative numbers of atoms present in a model or a diagrammatic representation",
            "4 Construct word equations and symbol equations to show how reactants form products, including state symbols",
            "5 Define the empirical formula of a compound as the simplest whole number ratio of the different atoms or ions in a compound",
            "6 Deduce the formula of an ionic compound from the relative numbers of the ions present in a model or a diagrammatic representation or from the charges on the ions",
            "7 Construct symbol equations with state symbols, including ionic equations",
            "8 Deduce the symbol equation with state symbols for a chemical reaction, given relevant information"]
        ],
        ["3.2 Relative masses of atoms and molecules",
            ["1 Describe relative atomic mass, Ar, as the average mass of the isotopes of an element compared to 1/12th of the mass of an atom of 12C",
            "2 Define relative molecular mass, Mr, as the sum of the relative atomic masses. Relative formula mass, Mr, will be used for ionic compounds",
            "3 Calculate reacting masses in simple proportions. Calculations will not involve the mole concept"]
        ],
        ["3.3 The mole and the Avogadro constant",
            ["1 State that concentration can be measured in g/dm3 or mol/dm3",
            "2 State that the mole, mol, is the unit of amount of substance and that one mole contains 6.02 × 10^23 particles, e.g. atoms, ions, molecules; this number is the Avogadro constant",
            "3 Use the relationship amount of substance (mol) = mass (g) / molar mass (g/mol) to calculate: (a) amount of substance (b) mass (c) molar mass (d) relative atomic mass or relative molecular/formula mass (e) number of particles, using the value of the Avogadro constant",
            "4 Use the molar gas volume, taken as 24 dm3 at room temperature and pressure, r.t.p., in calculations involving gases",
            "5 Calculate stoichiometric reacting masses, limiting reactants, volumes of gases at r.t.p., volumes of solutions and concentrations of solutions expressed in g/dm3 and mol/dm3, including conversion between cm3 and dm3",
            "6 Use experimental data from a titration to calculate the moles of solute, or the concentration or volume of a solution",
            "7 Calculate empirical formulae and molecular formulae, given appropriate data",
            "8 Calculate percentage yield, percentage composition by mass and percentage purity, given appropriate data"]
        ]
    ],
    ["4 Electrochemistry",
        ["4.1 Electrolysis",
            ["1 Define electrolysis as the decomposition of an ionic compound, when molten or in aqueous solution, by the passage of an electric current",
            "2 Identify in simple electrolytic cells: (a) the anode as the positive electrode (b) the cathode as the negative electrode (c) the electrolyte as the molten or aqueous substance that undergoes electrolysis",
            "3 Identify the products formed at the electrodes and describe the observations made during the electrolysis of: (a) molten lead(II) bromide (b) concentrated aqueous sodium chloride (c) dilute sulfuric acid using inert electrodes made of platinum or carbon/graphite",
            "4 State that metals or hydrogen are formed at the cathode and that non-metals (other than hydrogen) are formed at the anode",
            "5 Predict the identity of the products at each electrode for the electrolysis of a binary compound in the molten state",
            "6 State that metal objects are electroplated to improve their appearance and resistance to corrosion",
            "7 Describe how metals are electroplated",
            "8 Describe the transfer of charge during electrolysis to include: (a) the movement of electrons in the external circuit (b) the loss or gain of electrons at the electrodes (c) the movement of ions in the electrolyte",
            "9 Identify the products formed at the electrodes and describe the observations made during the electrolysis of aqueous copper(II) sulfate using inert carbon/graphite electrodes and when using copper electrodes",
            "10 Predict the identity of the products at each electrode for the electrolysis of a halide compound in dilute or concentrated aqueous solution",
            "11 Construct ionic half-equations for reactions at the anode (to show oxidation) and at the cathode (to show reduction)"]
        ],
        ["4.2 Hydrogen–oxygen fuel cells",
            ["1 State that a hydrogen–oxygen fuel cell uses hydrogen and oxygen to produce electricity with water as the only chemical product",
            "2 Describe the advantages and disadvantages of using hydrogen–oxygen fuel cells in comparison with gasoline/petrol engines in vehicles"]
        ]
    ],
    ["5 Chemical energetics",
        ["5.1 Exothermic and endothermic reactions",
            ["1 State that an exothermic reaction transfers thermal energy to the surroundings leading to an increase in the temperature of the surroundings",
            "2 State that an endothermic reaction takes in thermal energy from the surroundings leading to a decrease in the temperature of the surroundings",
            "3 Interpret reaction pathway diagrams showing exothermic and endothermic reactions",
            "4 State that the transfer of thermal energy during a reaction is called the enthalpy change, ∆H, of the reaction. ∆H is negative for exothermic reactions and positive for endothermic reactions",
            "5 Define activation energy, Ea, as the minimum energy that colliding particles must have to react",
            "6 Draw and label reaction pathway diagrams for exothermic and endothermic reactions using information provided, to include: (a) reactants (b) products (c) enthalpy change of the reaction, ∆H (d) activation energy, Ea",
            "7 State that bond breaking is an endothermic process and bond making is an exothermic process and explain the enthalpy change of a reaction in terms of bond breaking and bond making",
            "8 Calculate the enthalpy change of a reaction using bond energies"]
        ]
    ],
    ["6 Chemical reactions",
        ["6.1 Physical and chemical changes",
            ["1 Identify physical and chemical changes, and describe the differences between them"]
        ],
        ["6.2 Rate of reaction",
            ["1 Describe the effect on the rate of reaction of: (a) changing the concentration of solutions (b) changing the pressure of gases (c) changing the surface area of solids (d) changing the temperature (e) adding or removing a catalyst, including enzymes",
            "2 State that a catalyst increases the rate of a reaction and is unchanged at the end of a reaction",
            "3 Describe practical methods for investigating the rate of a reaction including change in mass of a reactant or a product and the formation of a gas",
            "4 Interpret data, including graphs, from rate of reaction experiments",
            "5 Describe collision theory in terms of: (a) number of particles per unit volume (b) frequency of collisions between particles (c) kinetic energy of particles (d) activation energy, Ea",
            "6 Describe and explain the effect on the rate of reaction of: (a) changing the concentration of solutions (b) changing the pressure of gases (c) changing the surface area of solids (d) changing the temperature (e) adding or removing a catalyst, including enzymes using collision theory",
            "7 State that a catalyst decreases the activation energy, Ea, of a reaction",
            "8 Evaluate practical methods for investigating the rate of a reaction including change in mass of a reactant or a product and the formation of a gas"]
        ],
        ["6.3 Reversible reactions and equilibrium",
            ["1 State that some chemical reactions are reversible as shown by the symbol ⇌",
            "2 Describe how changing the conditions can change the direction of a reversible reaction for: (a) the effect of heat on hydrated compounds (b) the addition of water to anhydrous compounds limited to copper(II) sulfate and cobalt(II) chloride",
            "3 State that a reversible reaction in a closed system is at equilibrium when: (a) the rate of the forward reaction is equal to the rate of the reverse reaction (b) the concentrations of reactants and products are no longer changing",
            "4 Predict and explain, for a reversible reaction, how the position of equilibrium is affected by: (a) changing temperature (b) changing pressure (c) changing concentration (d) using a catalyst using information provided",
            "5 State the symbol equation for the production of ammonia in the Haber process, N2(g) + 3H2(g) ⇌ 2NH3(g)",
            "6 State the sources of the hydrogen (methane) and nitrogen (air) in the Haber process",
            "7 State the typical conditions in the Haber process as 450 °C, 20 000 kPa / 200 atm and an iron catalyst",
            "8 State the symbol equation for the conversion of sulfur dioxide to sulfur trioxide in the Contact process, 2SO2(g) + O2(g) ⇌ 2SO3(g)",
            "9 State the sources of the sulfur dioxide (burning sulfur or roasting sulfide ores) and oxygen (air) in the Contact process",
            "10 State the typical conditions for the conversion of sulfur dioxide to sulfur trioxide in the Contact process as 450 °C, 200 kPa / 2 atm and a vanadium(V) oxide catalyst",
            "11 Explain, in terms of rate of reaction and position of equilibrium, why the typical conditions stated are used in the Haber process and in the Contact process, including safety considerations and economics"]
        ],
        ["6.4 Redox",
            ["1 Use a Roman numeral to indicate the oxidation number of an element in a compound",
            "2 Define redox reactions as involving simultaneous oxidation and reduction",
            "3 Define oxidation as gain of oxygen and reduction as loss of oxygen",
            "4 Identify redox reactions as reactions involving gain and loss of oxygen",
            "5 Identify oxidation and reduction in redox reactions",
            "6 Define oxidation in terms of: (a) loss of electrons (b) an increase in oxidation number",
            "7 Define reduction in terms of: (a) gain of electrons (b) a decrease in oxidation number",
            "8 Identify redox reactions as reactions involving gain and loss of electrons",
            "9 Identify redox reactions by changes in oxidation number using: (a) the oxidation number of elements in their uncombined state is zero (b) the oxidation number of a monatomic ion is the same as the charge on the ion (c) the sum of the oxidation numbers in a compound is zero (d) the sum of the oxidation numbers in an ion is equal to the charge on the ion",
            "10 Identify redox reactions by the colour changes involved when using acidified aqueous potassium manganate(VII) or aqueous potassium iodide",
            "11 Define an oxidising agent as a substance that oxidises another substance and is itself reduced",
            "12 Define a reducing agent as a substance that reduces another substance and is itself oxidised",
            "13 Identify oxidising agents and reducing agents in redox reactions"]
        ]
    ],
    ["7 Acids, bases and salts",
        ["7.1 The characteristic properties of acids and bases",
            ["1 Describe the characteristic properties of acids in terms of their reactions with: (a) metals (b) bases (c) carbonates",
            "2 Describe acids in terms of their effect on: (a) litmus (b) thymolphthalein (c) methyl orange",
            "3 State that bases are oxides or hydroxides of metals and that alkalis are soluble bases",
            "4 Describe the characteristic properties of bases in terms of their reactions with: (a) acids (b) ammonium salts",
            "5 Describe alkalis in terms of their effect on: (a) litmus (b) thymolphthalein (c) methyl orange",
            "6 State that aqueous solutions of acids contain H+ ions and aqueous solutions of alkalis contain OH– ions",
            "7 Describe how to compare hydrogen ion concentration, neutrality, relative acidity and relative alkalinity in terms of colour and pH using universal indicator paper",
            "8 Describe the neutralisation reaction between an acid and an alkali to produce water, H+ (aq) + OH– (aq) → H2O (l)",
            "9 Define acids as proton donors and bases as proton acceptors",
            "10 Define a strong acid as an acid that is completely dissociated in aqueous solution and a weak acid as an acid that is partially dissociated in aqueous solution",
            "11 State that hydrochloric acid is a strong acid, as shown by the symbol equation, HCl (aq) → H+(aq) + Cl –(aq)",
            "12 State that ethanoic acid is a weak acid, as shown by the symbol equation, CH3COOH(aq) ⇌ H+(aq) + CH3COO–(aq)"]
        ],
        ["7.2 Oxides",
            ["1 Classify oxides as acidic, including SO2 and CO2, or basic, including CuO and CaO, related to metallic and non-metallic character",
            "2 Describe amphoteric oxides as oxides that react with acids and with bases to produce a salt and water",
            "3 Classify Al2O3 and ZnO as amphoteric oxides"]
        ],
        ["7.3 Preparation of salts",
            ["1 Describe the preparation, separation and purification of soluble salts by reaction of an acid with: (a) an alkali by titration (b) excess metal (c) excess insoluble base (d) excess insoluble carbonate",
            "2 Describe the general solubility rules for salts: (a) sodium, potassium and ammonium salts are soluble (b) nitrates are soluble (c) chlorides are soluble, except lead and silver (d) sulfates are soluble, except barium, calcium and lead (e) carbonates are insoluble, except sodium, potassium and ammonium (f) hydroxides are insoluble, except sodium, potassium, ammonium and calcium (partially)",
            "3 Define a hydrated substance as a substance that is chemically combined with water and an anhydrous substance as a substance containing no water",
            "4 Describe the preparation of insoluble salts by precipitation",
            "5 Define the term water of crystallisation as the water molecules present in hydrated crystals, including CuSO4•5H2O and CoCl2•6H2O"]
        ]
    ],
    ["8 The Periodic Table",
        ["8.1 Arrangement of elements",
            ["1 Describe the Periodic Table as an arrangement of elements in periods and groups and in order of increasing proton number / atomic number",
            "2 Describe the change from metallic to non-metallic character across a period",
            "3 Describe the relationship between group number and the charge of the ions formed from elements in that group",
            "4 Explain similarities in the chemical properties of elements in the same group of the Periodic Table in terms of their electronic configuration",
            "5 Explain how the position of an element in the Periodic Table can be used to predict its properties",
            "6 Identify trends in groups, given information about the elements"]
        ],
        ["8.2 Group I properties",
            ["1 Describe the Group I alkali metals, lithium, sodium and potassium, as relatively soft metals with general trends down the group, limited to: (a) decreasing melting point (b) increasing density (c) increasing reactivity",
            "2 Predict the properties of other elements in Group I, given information about the elements"]
        ],
        ["8.3 Group VII properties",
            ["1 Describe the Group VII halogens, chlorine, bromine and iodine, as diatomic non-metals with general trends down the group, limited to: (a) increasing density (b) decreasing reactivity",
            "2 State the appearance of the halogens at r.t.p. as: (a) chlorine, a pale yellow-green gas (b) bromine, a red-brown liquid (c) iodine, a grey-black solid",
            "3 Describe and explain the displacement reactions of halogens with other halide ions",
            "4 Predict the properties of other elements in Group VII, given information about the elements"]
        ],
        ["8.4 Transition elements",
            ["1 Describe the transition elements as metals that: (a) have high densities (b) have high melting points (c) form coloured compounds (d) often act as catalysts as elements and in compounds",
            "2 Describe transition elements as having ions with variable oxidation numbers, including iron(II) and iron(III)"]
        ],
        ["8.5 Noble gases",
            ["1 Describe the Group VIII noble gases as unreactive, monatomic gases and explain this in terms of electronic configuration"]
        ]
    ],
    ["9 Metals",
        ["9.1 Properties of metals",
            ["1 Compare the general physical properties of metals and non-metals, including: (a) thermal conductivity (b) electrical conductivity (c) malleability and ductility (d) melting points and boiling points",
            "2 Describe the general chemical properties of metals, limited to their reactions with: (a) dilute acids (b) cold water and steam (c) oxygen"]
        ],
        ["9.2 Uses of metals",
            ["1 Describe the uses of metals in terms of their physical properties, including: (a) aluminium in the manufacture of aircraft because of its low density (b) aluminium in the manufacture of overhead electrical cables because of its low density and good electrical conductivity (c) aluminium in food containers because of its resistance to corrosion (d) copper in electrical wiring because of its good electrical conductivity and ductility"]
        ],
        ["9.3 Alloys and their properties",
            ["1 Describe an alloy as a mixture of a metal with other elements, including: (a) brass as a mixture of copper and zinc (b) stainless steel as a mixture of iron and other elements such as chromium, nickel and carbon",
            "2 State that alloys can be harder and stronger than the pure metals and are more useful",
            "3 Describe the uses of alloys in terms of their physical properties, including stainless steel in cutlery because of its hardness and resistance to rusting",
            "4 Identify representations of alloys from diagrams of structure",
            "5 Explain in terms of structure how alloys can be harder and stronger than the pure metals because the different sized atoms in alloys mean the layers can no longer slide over each other"]
        ],
        ["9.4 Reactivity series",
            ["1 State the order of the reactivity series as: potassium, sodium, calcium, magnesium, aluminium, carbon, zinc, iron, hydrogen, copper, silver, gold",
            "2 Describe the reactions, if any, of: (a) potassium, sodium and calcium with cold water (b) magnesium with steam (c) magnesium, zinc, iron, copper, silver and gold with dilute hydrochloric acid and explain these reactions in terms of the position of the metals in the reactivity series",
            "3 Deduce an order of reactivity from a given set of experimental results",
            "4 Describe the relative reactivities of metals in terms of their tendency to form positive ions, by displacement reactions, if any, with the aqueous ions of magnesium, zinc, iron, copper and silver",
            "5 Explain the apparent unreactivity of aluminium in terms of its oxide layer"]
        ],
        ["9.5 Corrosion of metals",
            ["1 State the conditions required for the rusting of iron and steel to form hydrated iron(III) oxide",
            "2 State some common barrier methods, including painting, greasing and coating with plastic",
            "3 Describe how barrier methods prevent rusting by excluding oxygen or water",
            "4 Describe the use of zinc in galvanising as an example of a barrier method and sacrificial protection",
            "5 Explain sacrificial protection in terms of the reactivity series and in terms of electron loss"]
        ],
        ["9.6 Extraction of metals",
            ["1 Describe the ease in obtaining metals from their ores, related to the position of the metal in the reactivity series",
            "2 Describe the extraction of iron from hematite in the blast furnace, limited to: (a) the burning of carbon (coke) to provide heat and produce carbon dioxide (b) the reduction of carbon dioxide to carbon monoxide (c) the reduction of iron(III) oxide by carbon monoxide (d) the thermal decomposition of calcium carbonate / limestone to produce calcium oxide (e) the formation of slag Symbol equations are not required",
            "3 State that the main ore of aluminium is bauxite and that aluminium is extracted by electrolysis",
            "4 State the symbol equations for the extraction of iron from hematite (a) C + O2 → CO2 (b) C + CO2 → 2CO (c) Fe2O3 + 3CO → 2Fe + 3CO2 (d) CaCO3 → CaO + CO2 (e) CaO + SiO2 → CaSiO3",
            "5 Describe the extraction of aluminium from purified bauxite / aluminium oxide, including: (a) the role of cryolite (b) why the carbon anodes need to be regularly replaced (c) the reactions at the electrodes, including ionic half-equations Details of the purification of bauxite are not required"]
        ]
    ],
    ["10 Chemistry of the environment",
        ["10.1 Water",
            ["1 Describe chemical tests for the presence of water using anhydrous cobalt(II) chloride and anhydrous copper(II) sulfate",
            "2 Describe how to test for the purity of water using melting point and boiling point",
            "3 Explain that distilled water is used in practical chemistry rather than tap water because it contains fewer chemical impurities",
            "4 State that water from natural sources may contain substances, including: (a) dissolved oxygen (b) metal compounds (c) plastics (d) sewage (e) harmful microbes (f) nitrates from fertilisers (g) phosphates from fertilisers and detergents",
            "5 State that some of these substances are beneficial, including: (a) dissolved oxygen for aquatic life (b) some metal compounds provide essential minerals for life",
            "6 State that some of these substances are potentially harmful, including: (a) some metal compounds are toxic (b) some plastics harm aquatic life (c) sewage contains harmful microbes which cause disease (d) nitrates and phosphates lead to deoxygenation of water and damage to aquatic life Details of the eutrophication process are not required",
            "7 Describe the treatment of the domestic water supply in terms of: (a) sedimentation and filtration to remove solids (b) use of carbon to remove tastes and odours (c) chlorination to kill microbes"]
        ],
        ["10.2 Fertilisers",
            ["1 State that ammonium salts and nitrates are used as fertilisers",
            "2 Describe the use of NPK fertilisers to provide the elements nitrogen, phosphorus and potassium for improved plant growth"]
        ],
        ["10.3 Air quality and climate",
            ["1 State the composition of clean, dry air as approximately 78% nitrogen, N2, 21% oxygen, O2 and the remainder as a mixture of noble gases and carbon dioxide, CO2",
            "2 State the source of each of these air pollutants, limited to: (a) carbon dioxide from the complete combustion of carbon-containing fuels (b) carbon monoxide and particulates from the incomplete combustion of carbon-containing fuels (c) methane from the decomposition of vegetation and waste gases from digestion in animals (d) oxides of nitrogen from car engines (e) sulfur dioxide from the combustion of fossil fuels which contain sulfur compounds",
            "3 State the adverse effect of these air pollutants, limited to: (a) carbon dioxide: higher levels of carbon dioxide leading to increased global warming, which leads to climate change (b) carbon monoxide: toxic gas (c) particulates: increased risk of respiratory problems and cancer (d) methane: higher levels of methane leading to increased global warming, which leads to climate change (e) oxides of nitrogen: acid rain, photochemical smog and respiratory problems (f) sulfur dioxide: acid rain",
            "4 State and explain strategies to reduce the effects of these environmental issues, limited to: (a) climate change: planting trees, reduction in livestock farming, decreasing use of fossil fuels, increasing use of hydrogen and renewable energy, e.g. wind, solar (b) acid rain: use of catalytic converters in vehicles, reducing emissions of sulfur dioxide by using low-sulfur fuels and flue gas desulfurisation with calcium oxide",
            "5 Describe photosynthesis as the reaction between carbon dioxide and water to produce glucose and oxygen in the presence of chlorophyll and using energy from light",
            "6 State the word equation for photosynthesis, carbon dioxide + water → glucose + oxygen",
            "7 Describe how the greenhouse gases carbon dioxide and methane cause global warming, limited to: (a) the absorption, reflection and emission of thermal energy (b) reducing thermal energy loss to space",
            "8 Explain how oxides of nitrogen form in car engines and describe their removal by catalytic converters, e.g. 2CO + 2NO → 2CO2 + N2",
            "9 State the symbol equation for photosynthesis, 6CO2 + 6H2O → C6H12O6 + 6O2"]
        ]
    ],
    ["11 Organic chemistry",
        ["11.1 Formulae, functional groups and terminology",
            ["1 Draw and interpret the displayed formula of a molecule to show all the atoms and all the bonds",
            "2 Write and interpret general formulae of compounds in the same homologous series, limited to: (a) alkanes, CnH2n+2 (b) alkenes, CnH2n (c) alcohols, CnH2n+1OH (d) carboxylic acids, CnH2n+1COOH",
            "3 Identify a functional group as an atom or group of atoms that determine the chemical properties of a homologous series",
            "4 State that a homologous series is a family of similar compounds with similar chemical properties due to the presence of the same functional group",
            "5 State that a saturated compound has molecules in which all carbon–carbon bonds are single bonds",
            "6 State that an unsaturated compound has molecules in which one or more carbon–carbon bonds are not single bonds",
            "7 State that a structural formula is an unambiguous description of the way the atoms in a molecule are arranged, including CH2=CH2, CH3CH2OH, CH3COOCH3",
            "8 Define structural isomers as compounds with the same molecular formula, but different structural formulae, including C4H10 as CH3CH2CH2CH3 and CH3CH(CH3)CH3 and C4H8 as CH3CH2CH=CH2 and CH3CH=CHCH3",
            "9 Describe the general characteristics of a homologous series as: (a) having the same functional group (b) having the same general formula (c) differing from one member to the next by a –CH2– unit (d) displaying a trend in physical properties (e) sharing similar chemical properties"]
        ],
        ["11.2 Naming organic compounds",
            ["1 Name and draw the displayed formulae of: (a) methane and ethane (b) ethene (c) ethanol (d) ethanoic acid (e) the products of the reactions stated in sections 11.4–11.7",
            "2 State the type of compound present, given a chemical name ending in -ane, -ene, -ol, or -oic acid or from a molecular formula or displayed formula",
            "3 Name and draw the structural and displayed formulae of unbranched: (a) alkanes (b) alkenes, including but-1-ene and but-2-ene (c) alcohols, including propan-1-ol, propan-2-ol, butan-1-ol and butan-2-ol (d) carboxylic acids containing up to four carbon atoms per molecule",
            "4 Name and draw the displayed formulae of the unbranched esters which can be made from unbranched alcohols and carboxylic acids, each containing up to four carbon atoms"]
        ],
        ["11.3 Fuels",
            ["1 Name the fossil fuels: coal, natural gas and petroleum",
            "2 Name methane as the main constituent of natural gas",
            "3 State that hydrocarbons are compounds that contain hydrogen and carbon only",
            "4 State that petroleum is a mixture of hydrocarbons",
            "5 Describe the separation of petroleum into useful fractions by fractional distillation",
            "6 Describe how the properties of fractions obtained from petroleum change from the bottom to the top of the fractionating column, limited to: (a) decreasing chain length (b) higher volatility (c) lower boiling points (d) lower viscosity",
            "7 Name the uses of the fractions as: (a) refinery gas fraction for gas used in heating and cooking (b) gasoline/petrol fraction for fuel used in cars (c) naphtha fraction as a chemical feedstock (d) kerosene/paraffin fraction for jet fuel (e) diesel oil/gas oil fraction for fuel used in diesel engines (f) fuel oil fraction for fuel used in ships and home heating systems (g) lubricating oil fraction for lubricants, waxes and polishes (h) bitumen fraction for making roads"]
        ],
        ["11.4 Alkanes",
            ["1 State that the bonding in alkanes is single covalent and that alkanes are saturated hydrocarbons",
            "2 Describe the properties of alkanes as being generally unreactive, except in terms of combustion and substitution by chlorine",
            "3 State that in a substitution reaction one atom or group of atoms is replaced by another atom or group of atoms",
            "4 Describe the substitution reaction of alkanes with chlorine as a photochemical reaction, with ultraviolet light providing the activation energy, Ea, and draw the structural or displayed formulae of the products, limited to monosubstitution"]
        ],
        ["11.5 Alkenes",
            ["1 State that the bonding in alkenes includes a double carbon–carbon covalent bond and that alkenes are unsaturated hydrocarbons",
            "2 Describe the manufacture of alkenes and hydrogen by the cracking of larger alkane molecules using a high temperature and a catalyst",
            "3 Describe the reasons for the cracking of larger alkane molecules",
            "4 Describe the test to distinguish between saturated and unsaturated hydrocarbons by their reaction with aqueous bromine",
            "5 State that in an addition reaction only one product is formed",
            "6 Describe the properties of alkenes in terms of addition reactions with: (a) bromine or aqueous bromine (b) hydrogen in the presence of a nickel catalyst (c) steam in the presence of an acid catalyst and draw the structural or displayed formulae of the products"]
        ],
        ["11.6 Alcohols",
            ["1 Describe the manufacture of ethanol by: (a) fermentation of aqueous glucose at 25–35 °C in the presence of yeast and in the absence of oxygen (b) catalytic addition of steam to ethene at 300 °C and 6000 kPa/60 atm in the presence of an acid catalyst",
            "2 Describe the combustion of ethanol",
            "3 State the uses of ethanol as: (a) a solvent (b) a fuel",
            "4 Describe the advantages and disadvantages of the manufacture of ethanol by: (a) fermentation (b) catalytic addition of steam to ethene"]
        ],
        ["11.7 Carboxylic acids",
            ["1 Describe the reaction of ethanoic acid with: (a) metals (b) bases (c) carbonates including names and formulae of the salts produced",
            "2 Describe the formation of ethanoic acid by the oxidation of ethanol: (a) with acidified aqueous potassium manganate(VII) (b) by bacterial oxidation during vinegar production",
            "3 Describe the reaction of a carboxylic acid with an alcohol using an acid catalyst to form an ester"]
        ],
        ["11.8 Polymers",
            ["1 Define polymers as large molecules built up from many smaller molecules called monomers",
            "2 Describe the formation of poly(ethene) as an example of addition polymerisation using ethene monomers",
            "3 State that plastics are made from polymers",
            "4 Describe how the properties of plastics have implications for their disposal",
            "5 Describe the environmental challenges caused by plastics, limited to: (a) disposal in landfill sites (b) accumulation in oceans (c) formation of toxic gases from burning",
            "6 Identify the repeat units and/or linkages in addition polymers and in condensation polymers",
            "7 Deduce the structure or repeat unit of an addition polymer from a given alkene and vice versa",
            "8 Deduce the structure or repeat unit of a condensation polymer from given monomers and vice versa, limited to: (a) polyamides from a dicarboxylic acid and a diamine (b) polyesters from a dicarboxylic acid and a diol",
            "9 Describe the differences between addition and condensation polymerisation",
            "10 Describe and draw the structure of: (a) nylon, a polyamide (b) PET, a polyester The full name for PET, polyethylene terephthalate, is not required",
            "11 State that PET can be converted back into monomers and re-polymerised",
            "12 Describe proteins as natural polyamides and that they are formed from amino acid monomers with the general structure: H2N-CHR-COOH where R represents different types of side chain",
            "13 Describe and draw the structure of proteins as: -CONH- linkages in polypeptides formed by condensation polymerisation"]
        ]
    ],
    ["12 Experimental techniques and chemical analysis",
        ["12.1 Experimental design",
            ["1 Name appropriate apparatus for the measurement of time, temperature, mass and volume, including: (a) stopwatches (b) thermometers (c) balances (d) burettes (e) volumetric pipettes (f) measuring cylinders (g) gas syringes",
            "2 Suggest advantages and disadvantages of experimental methods and apparatus",
            "3 Describe a: (a) solvent as a substance that dissolves a solute (b) solute as a substance that is dissolved in a solvent (c) solution as a mixture of one or more solutes dissolved in a solvent (d) saturated solution as a solution containing the maximum concentration of a solute dissolved in the solvent at a specified temperature (e) residue as a substance that remains after evaporation, distillation, filtration or any similar process (f) filtrate as a liquid or solution that has passed through a filter"]
        ],
        ["12.2 Acid–base titrations",
            ["1 Describe an acid–base titration to include the use of a: (a) burette (b) volumetric pipette (c) suitable indicator",
            "2 Describe how to identify the end-point of a titration using an indicator"]
        ],
        ["12.3 Chromatography",
            ["1 Describe how paper chromatography is used to separate mixtures of soluble coloured substances, using a suitable solvent",
            "2 Interpret simple chromatograms to identify: (a) unknown substances by comparison with known substances (b) pure and impure substances",
            "3 Describe how paper chromatography is used to separate mixtures of soluble colourless substances, using a suitable solvent and a locating agent Knowledge of specific locating agents is not required",
            "4 State and use the equation for Rf: Rf = distance travelled by substance / distance travelled by solvent"]
        ],
        ["12.4 Separation and purification",
            ["1 Describe and explain methods of separation and purification using: (a) a suitable solvent (b) filtration (c) crystallisation (d) simple distillation (e) fractional distillation",
            "2 Suggest suitable separation and purification techniques, given information about the substances involved",
            "3 Identify substances and assess their purity using melting point and boiling point information"]
        ],
        ["12.5 Identification of ions and gases",
            ["1 Describe tests to identify the anions: (a) carbonate, CO3 2−, by reaction with dilute acid and then testing for carbon dioxide gas (b) chloride, Cl −, bromide, Br −, and iodide, I −, by acidifying with dilute nitric acid then adding aqueous silver nitrate (c) nitrate, NO3 −, reduction with aluminium foil and aqueous sodium hydroxide and then testing for ammonia gas (d) sulfate, SO4 2−, by acidifying with dilute nitric acid and then adding aqueous barium nitrate (e) sulfite, SO3 2−, by reaction with acidified aqueous potassium manganate(VII)",
            "2 Describe tests using aqueous sodium hydroxide and aqueous ammonia to identify the aqueous cations: (a) aluminium, Al 3+ (b) ammonium, NH4 + (c) calcium, Ca2+ (d) chromium(III), Cr3+ (e) copper(II), Cu2+ (f) iron(II), Fe2+ (g) iron(III), Fe3+ (h) zinc, Zn2+",
            "3 Describe tests to identify the gases: (a) ammonia, NH3, using damp red litmus paper (b) carbon dioxide, CO2, using limewater (c) chlorine, Cl 2, using damp litmus paper (d) hydrogen, H2, using a lighted splint (e) oxygen, O2, using a glowing splint (f) sulfur dioxide, SO2, using acidified aqueous potassium manganate(VII)",
            "4 Describe the use of a flame test to identify the cations: (a) lithium, Li+ (b) sodium, Na+ (c) potassium, K+ (d) calcium, Ca2+ (e) barium, Ba2+ (f) copper(II), Cu2+"]
        ]
    ]
]

# Assume syllabus_details is already defined here

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class AccessCodeDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Access Code")
        self.setGeometry(100, 100, 400, 200)
        layout = QtWidgets.QVBoxLayout()

        self.access_code_input = QtWidgets.QLineEdit()
        self.access_code_input.setPlaceholderText("Enter Access Code")
        layout.addWidget(self.access_code_input)

        self.verify_button = QtWidgets.QPushButton("Verify")
        self.verify_button.clicked.connect(self.verify_access_code)
        layout.addWidget(self.verify_button)

        self.setLayout(layout)

    def verify_access_code(self):
        access_code = self.access_code_input.text()
        if access_code:
            try:
                response = requests.post('http://127.0.0.1:5000/verify_access_code', json={'access_code': access_code})
                response.raise_for_status()
                response_json = response.json()
                if response.status_code == 200:
                    QtWidgets.QMessageBox.information(self, "Success", "Access granted.")
                    self.accept()
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", response_json.get('message', 'Invalid or expired access code.'))
            except requests.exceptions.RequestException as e:
                QtWidgets.QMessageBox.warning(self, "Error", f"Server error: {e}")
            except requests.exceptions.JSONDecodeError:
                QtWidgets.QMessageBox.warning(self, "Error", "Invalid response from server.")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Access code is required.")

class HelpPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self.setGeometry(100, 100, 600, 400)
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("Help Information:\nThis is a detailed help page with instructions on how to use the application.")
        layout.addWidget(label)
        self.setLayout(layout)

class AboutPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setGeometry(100, 100, 600, 400)
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("About this Application:\nVersion 1.0\nDeveloped by: Laksh Sarda")
        layout.addWidget(label)
        self.setLayout(layout)

class MainPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        self.question_paper_button = QtWidgets.QPushButton("Generate Question Paper")
        self.question_paper_button.setMinimumHeight(80)
        self.question_paper_button.setStyleSheet(self.get_button_style())
        layout.addWidget(self.question_paper_button)
        self.question_paper_button.clicked.connect(self.show_paper_generation_options)

        self.help_button = QtWidgets.QPushButton("Help")
        self.help_button.setMinimumHeight(80)
        self.help_button.setStyleSheet(self.get_button_style())
        layout.addWidget(self.help_button)
        self.help_button.clicked.connect(self.open_help_page)

        self.about_button = QtWidgets.QPushButton("About")
        self.about_button.setMinimumHeight(80)
        self.about_button.setStyleSheet(self.get_button_style())
        layout.addWidget(self.about_button)
        self.about_button.clicked.connect(self.open_about_page)

        self.setLayout(layout)

    def get_button_style(self):
        return """
            QPushButton {
                background-color: #5A5A5A;
                color: #FFFFFF;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #5A5A5A;
            }
            QPushButton:hover {
                background-color: #34ebb1;
                border: 2px solid #34ebb1;
            }
            QPushButton:pressed {
                background-color: #34ebb1;
                border: 2px solid #34ebb1;
            }
        """

    def open_help_page(self):
        self.help_page = HelpPage()
        self.help_page.show()

    def open_about_page(self):
        self.about_page = AboutPage()
        self.about_page.show()

    def show_paper_generation_options(self):
        self.paper_gen_window = PaperGenerationWindow()
        self.paper_gen_window.show()

class PaperGenerationWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paper Generation")
        self.setGeometry(100, 100, 800, 600)
        layout = QtWidgets.QVBoxLayout()

        self.generate_paper_2_button = QtWidgets.QPushButton("Generate Paper 2 (MCQ)")
        self.generate_paper_2_button.setMinimumHeight(80)
        self.generate_paper_2_button.setStyleSheet(self.get_button_style())
        self.generate_paper_2_button.clicked.connect(self.generate_paper_2)
        layout.addWidget(self.generate_paper_2_button)

        self.setLayout(layout)

    def get_button_style(self):
        return """
            QPushButton {
                background-color: #5A5A5A;
                color: #FFFFFF;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #5A5A5A;
            }
            QPushButton:hover {
                background-color: #34ebb1;
                border: 2px solid #34ebb1;
            }
            QPushButton:pressed {
                background-color: #34ebb1;
                border: 2px solid #34ebb1;
            }
        """

    def generate_paper_2(self):
        self.paper_2_window = Paper2Window()
        self.paper_2_window.show()

class Paper2Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generate Paper 2 (MCQ)")
        self.setGeometry(100, 100, 800, 600)
        self.total_marks = 0
        self.weightages = []
        self.topics = []
        self.included_questions = set()  # Track included questions to avoid redundancy

        layout = QtWidgets.QVBoxLayout()

        self.marks_input = QtWidgets.QLineEdit()
        self.marks_input.setPlaceholderText("Enter number of marks the paper should be for:")
        self.marks_input.setMinimumHeight(35)
        self.marks_input.textChanged.connect(self.update_marks)
        layout.addWidget(self.marks_input)

        layout.addSpacerItem(QtWidgets.QSpacerItem(20, 50))

        self.topic_choice = QtWidgets.QComboBox()
        self.topic_choice.setMinimumHeight(50)
        
        # List of units with their names
        unit_options = [
            "1.1 Solids, liquids and gases",
            "1.2 Diffusion",
            "2.1 Elements, compounds and mixtures",
            "2.2 Atomic structure and the Periodic Table",
            "2.3 Isotopes",
            "2.4 Ions and ionic bonds",
            "2.5 Simple molecules and covalent bonds",
            "2.6 Giant covalent structures",
            "2.7 Metallic bonding",
            "3.1 Formulae",
            "3.2 Relative masses of atoms and molecules",
            "3.3 The mole and the Avogadro constant",
            "4.1 Electrolysis",
            "4.2 Hydrogen–oxygen fuel cells",
            "5.1 Exothermic and endothermic reactions",
            "6.1 Physical and chemical changes",
            "6.2 Rate of reaction",
            "6.3 Reversible reactions and equilibrium",
            "6.4 Redox",
            "7.1 The characteristic properties of acids and bases",
            "7.2 Oxides",
            "7.3 Preparation of salts",
            "8.1 Arrangement of elements",
            "8.2 Group I properties",
            "8.3 Group VII properties",
            "8.4 Transition elements",
            "8.5 Noble gases",
            "9.1 Properties of metals",
            "9.2 Uses of metals",
            "9.3 Alloys and their properties",
            "9.4 Reactivity series",
            "9.5 Corrosion of metals",
            "9.6 Extraction of metals",
            "10.1 Water",
            "10.2 Fertilisers",
            "10.3 Air quality and climate",
            "11.1 Formulae, functional groups and terminology",
            "11.2 Naming organic compounds",
            "11.3 Fuels",
            "11.4 Alkanes",
            "11.5 Alkenes",
            "11.6 Alcohols",
            "11.7 Carboxylic acids",
            "11.8 Polymers",
            "12.1 Experimental design",
            "12.2 Acid–base titrations",
            "12.3 Chromatography",
            "12.4 Separation and purification",
            "12.5 Identification of ions and gases"
        ]

        self.topic_choice.addItems(unit_options)
        layout.addWidget(self.topic_choice)

        layout.addSpacerItem(QtWidgets.QSpacerItem(20, 50))

        self.weightage_input = QtWidgets.QLineEdit()
        self.weightage_input.setPlaceholderText("Enter weightage of topic:")
        self.weightage_input.setMinimumHeight(35)
        layout.addWidget(self.weightage_input)

        layout.addSpacerItem(QtWidgets.QSpacerItem(20, 50))

        self.add_topic_button = QtWidgets.QPushButton("Add new topic")
        self.add_topic_button.setMinimumHeight(50)
        self.add_topic_button.setStyleSheet(self.get_button_style())
        self.add_topic_button.clicked.connect(self.add_topic)
        layout.addWidget(self.add_topic_button)

        layout.addSpacerItem(QtWidgets.QSpacerItem(20, 50))

        self.marks_generated_label = QtWidgets.QLabel("Marks generated: 0")
        layout.addWidget(self.marks_generated_label)

        self.marks_remaining_label = QtWidgets.QLabel("Marks remaining: 0")
        layout.addWidget(self.marks_remaining_label)

        layout.addSpacerItem(QtWidgets.QSpacerItem(20, 50))

        self.process_button = QtWidgets.QPushButton("Process")
        self.process_button.setStyleSheet(self.get_button_style())
        self.process_button.setMinimumHeight(50)
        self.process_button.setEnabled(False)
        self.process_button.clicked.connect(self.process_paper)
        layout.addWidget(self.process_button)

        layout.addSpacerItem(QtWidgets.QSpacerItem(20, 50))

        self.restart_button = QtWidgets.QPushButton("Restart Generation")
        self.restart_button.setMinimumHeight(50)
        self.restart_button.setStyleSheet(self.get_button_style())
        self.restart_button.clicked.connect(self.restart_generation)
        layout.addWidget(self.restart_button)

        self.setLayout(layout)

    def get_button_style(self):
        return """
            QPushButton {
                background-color: #5A5A5A;
                color: #FFFFFF;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #5A5A5A;
            }
            QPushButton:hover {
                background-color: #34ebb1;
                border: 2px solid #34ebb1;
            }
            QPushButton:pressed {
                background-color: #34ebb1;
                border: 2px solid #34ebb1;
            }
        """

    def update_marks(self):
        try:
            self.total_marks = int(self.marks_input.text())
        except ValueError:
            self.total_marks = 0
        self.update_marks_remaining()

    def add_topic(self):
        try:
            weightage = int(self.weightage_input.text())
            topic = self.topic_choice.currentText()
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid number for weightage.")
            return

        potential_marks_generated = (sum(self.weightages) + weightage) / 100 * self.total_marks

        if potential_marks_generated > self.total_marks:
            QMessageBox.warning(self, "Input Error", "You are trying to create a paper for more marks than you asked for!")
            return

        self.weightages.append(weightage)
        self.topics.append(topic)
        self.update_marks_remaining()

        if sum(self.weightages) == 100:
            self.process_button.setEnabled(True)
        else:
            self.process_button.setEnabled(False)

    def update_marks_remaining(self):
        marks_generated = (sum(self.weightages) / 100) * self.total_marks
        self.marks_generated_label.setText(f"Marks generated: {marks_generated:.2f}")
        marks_remaining = self.total_marks - marks_generated
        self.marks_remaining_label.setText(f"Marks remaining: {marks_remaining:.2f}")

    def process_paper(self):
        file_dialog = QFileDialog()
        options = file_dialog.options()
        filename, _ = file_dialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if filename:
            self.generate_custom_pdf(filename)
            self.upload_to_firebase(filename)
            QMessageBox.information(self, "Success", f"PDF generated and uploaded as {os.path.basename(filename)}")

    def populate_topic_choice(self):
        self.topic_choice.addItem("Choose topic")
        for unit in syllabus_details:
            unit_number, unit_name = unit[0].split(' ', 1)
            for subunit in unit[1:]:
                subunit_number = subunit[0].split(' ')[0]
                self.topic_choice.addItem(f"{unit_number}.{subunit_number} {unit_name}")

    def generate_custom_pdf(self, filename):
        selected_unit_details = []
        for topic in self.topics:
            for detail in syllabus_details:
                if detail[0].startswith(topic.split('.')[0]):
                    for sub_detail in detail[1:]:
                        if sub_detail[0].startswith(topic):
                            selected_unit_details.extend(sub_detail[1])

        questions = []
        pdf_files = [f for f in os.listdir('past_papers') if f.endswith('.pdf')]
        pdf_file_questions = {}

        for pdf_file in pdf_files:
            pdf_path = os.path.join('past_papers', pdf_file)
            extracted_questions = extract_questions_from_pdf(pdf_path)
            pdf_file_questions[pdf_file] = extracted_questions
            questions.extend(extracted_questions)

        similarity_scores = calculate_similarity_st(selected_unit_details, questions)

        question_marks = 0
        processed_questions = set()
        output_pdf_paths = []
        matched_criteria = []
        marks_needed = {topic: (self.weightages[i] / 100) * self.total_marks for i, topic in enumerate(self.topics)}
        marks_allocated = {topic: 0 for topic in self.topics}

        while question_marks < self.total_marks and question_marks < len(questions):
            for question_index, question in enumerate(questions):
                if question_index in processed_questions:
                    continue

                question_number = int(re.findall(r'^\d+', question)[0])
                if question_number in [1, 2, 3, 4]:
                    continue

                if question in self.included_questions:
                    continue

                max_score = 0
                best_match = None
                best_topic = None

                for i, score in enumerate(similarity_scores):
                    if score[question_index] > max_score:
                        max_score = score[question_index]
                        best_match = selected_unit_details[i]
                        best_topic = self.topics[i % len(self.topics)]

                if max_score > 0.595 and marks_allocated[best_topic] < marks_needed[best_topic]:
                    for pdf_file, extracted_questions in pdf_file_questions.items():
                        if question in extracted_questions:
                            pdf_path = os.path.join('past_papers', pdf_file)
                            break

                    coordinates = locate_question(pdf_path, question)
                    if coordinates:
                        short_question_id = hashlib.md5(question.encode()).hexdigest()[:8]
                        output_pdf_path = f"output_{pdf_file}_{short_question_id}.pdf"
                        if create_output_pdf(pdf_path, coordinates, output_pdf_path):
                            img = Image.open(f"page_{coordinates['page_start']}.png")
                            img = ImageOps.grayscale(img)
                            extracted_text = pytesseract.image_to_string(img)
                            word_count = len(extracted_text.split())
                            question_number_count = len(re.findall(r'^\d+\s', extracted_text, re.MULTILINE))
                            if word_count >= 10 and question_number_count == 1:
                                paper_code = os.path.splitext(os.path.basename(pdf_path))[0]
                                output_pdf_paths.append(output_pdf_path)
                                matched_criteria.append((question, best_match, max_score, paper_code))
                                question_marks += 1
                                marks_allocated[best_topic] += 1
                                processed_questions.add(question_index)
                                self.included_questions.add(question)  # Add the question to the set
                                print(f"Question: {question}\nMatched Syllabus Criteria: {best_match}\nCosine Similarity Score: {max_score:.4f}\nPaper Code: {paper_code}\n")
                            else:
                                os.remove(output_pdf_path)
                    if question_marks >= self.total_marks:
                        break

        combined_output_pdf_path = filename
        if output_pdf_paths:
            combined_doc = fitz.open()
            for path in output_pdf_paths:
                combined_doc.insert_pdf(fitz.open(path))
            combined_doc.save(combined_output_pdf_path)
            combined_doc.close()

            for path in output_pdf_paths:
                if os.path.exists(path):
                    os.remove(path)

            print(f"Output PDF created at {combined_output_pdf_path}")
        else:
            print("Failed to create a combined output PDF. No valid questions found that meet the criteria.")

    def upload_to_firebase(self, filename):
        bucket = storage.bucket()
        blob = bucket.blob(f'papers/{os.path.basename(filename)}')
        blob.upload_from_filename(filename)

    def restart_generation(self):
        self.total_marks = 0
        self.weightages.clear()
        self.topics.clear()
        self.included_questions.clear()  # Reset the included questions set
        self.marks_input.clear()
        self.topic_choice.setCurrentIndex(0)
        self.weightage_input.clear()
        self.marks_generated_label.setText("Marks generated: 0")
        self.marks_remaining_label.setText("Marks remaining: 0")
        self.process_button.setEnabled(False)



def extract_questions_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    questions = []

    question_start_regex = re.compile(r'^\d+\s')  # Matches question numbers at the beginning of a line

    for page_num in range(1, doc.page_count - 1):  # Ignoring the first and last page
        page = doc[page_num]
        text = page.get_text("text")
        
        lines = text.split('\n')
        current_question = ""
        
        for line in lines:
            if re.match(r'© UCLES', line) or re.match(r'\[Turn over\]', line):
                continue
            
            if re.match(r'^[A-D]\s', line):
                continue

            # Ensure the number is between 1 and 40
            match = question_start_regex.match(line)
            if match:
                question_number = int(match.group().strip())
                if 1 <= question_number <= 40:
                    if current_question:
                        questions.append(current_question.strip())
                    current_question = line
                else:
                    current_question += " " + line
            else:
                current_question += " " + line

        if current_question:
            questions.append(current_question.strip())
    
    filtered_questions = []
    for question in questions:
        question = re.sub(r'© UCLES.*', '', question)
        question = re.sub(r'\[Turn over\]', '', question)
        question = question.strip()
        if question and not re.match(r'^\d{1,2}\s+\d{4}/\d{2}/[A-Z]/\d{2}$', question):
            filtered_questions.append(question)
    
    return filtered_questions

def calculate_similarity_st(syllabus_details, questions):
    model = SentenceTransformer('paraphrase-mpnet-base-v2')
    
    syllabus_embeddings = model.encode(syllabus_details, convert_to_tensor=True)
    question_embeddings = model.encode(questions, convert_to_tensor=True)
    
    similarity_scores = util.pytorch_cos_sim(syllabus_embeddings, question_embeddings)
    
    return similarity_scores.cpu().numpy()

def locate_question(pdf_path, question):
    doc = fitz.open(pdf_path)
    question_number = int(re.findall(r'^\d+', question)[0])
    question_start_regex = re.compile(rf'^{question_number}\s')
    question_end_regex = re.compile(rf'^{question_number + 1}\s')

    question_start = None
    question_end = None
    page_number_start = None
    page_number_end = None

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        lines = text.splitlines()

        for line_num, line in enumerate(lines):
            if question_start is None and re.match(question_start_regex, line):
                search_result = page.search_for(line)
                if search_result:
                    question_start = search_result[0]
                    page_number_start = page_num
                    continue

            if question_start is not None and re.match(question_end_regex, line):
                search_result = page.search_for(line)
                if search_result:
                    question_end = search_result[0]
                    page_number_end = page_num
                    break

        if question_start and question_end:
            break

    if not question_start:
        return None

    if not question_end:
        question_end = fitz.Rect(question_start.x0, question_start.y1, page.rect.width, page.rect.height)
        page_number_end = page_number_start

    return {
        'start': question_start,
        'end': question_end,
        'page_start': page_number_start,
        'page_end': page_number_end
    }

def create_output_pdf(pdf_path, coordinates, output_pdf_path):
    doc = fitz.open(pdf_path)
    c = canvas.Canvas(output_pdf_path)
    valid_pages = 0

    for page_num in range(coordinates['page_start'], coordinates['page_end'] + 1):
        page = doc.load_page(page_num)
        if page_num == coordinates['page_start']:
            rect = fitz.Rect(0, coordinates['start'].y0, page.rect.width, page.rect.height)
            if page_num == coordinates['page_end']:
                rect = fitz.Rect(0, coordinates['start'].y0, page.rect.width, coordinates['end'].y0)
        elif page_num == coordinates['page_end']:
            rect = fitz.Rect(0, 0, page.rect.width, coordinates['end'].y0)
        else:
            rect = fitz.Rect(0, 0, page.rect.width, page.rect.height)

        if rect.width <= 0 or rect.height <= 0:
            continue

        pix = page.get_pixmap(clip=rect)
        img_path = f"page_{page_num}.png"
        pix.save(img_path)

        img = Image.open(img_path)
        img = ImageOps.grayscale(img)
        extracted_text = pytesseract.image_to_string(img)
        lines = extracted_text.split('\n')
        word_count = len(extracted_text.split())
        line_count = len([line for line in lines if line.strip() != ""])

        question_number_count = len(re.findall(r'^\d+\s', extracted_text, re.MULTILINE))

        # Validation to discard images with less than 10 words, containing more than one question,
        # or containing less than 2 lines of text
        if word_count < 10 or question_number_count > 1 or line_count < 2:
            os.remove(img_path)
            continue

        img_width, img_height = img.size
        c.setPageSize((img_width, img_height))
        c.drawImage(img_path, 0, 0, img_width, img_height)
        c.showPage()
        valid_pages += 1

    c.save()
    if valid_pages > 0:
        return True
    else:
        return False

def send_otp(email):
    otp = ''.join(random.choices(string.digits, k=6))
    ref = db.reference('otps')
    ref.push({
        'email': email,
        'otp': otp
    })

    sender_email = "lakshsarda137@gmail.com"
    app_password = "snft mjww smag kump"
    recipient_email = email
    message = MIMEText(f"Your OTP code is: {otp}")
    message['Subject'] = "OTP Verification"
    message['From'] = sender_email
    message['To'] = recipient_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
    except Exception as e:
        print("Failed to send email:", e)

class ResetPasswordDialog(QtWidgets.QDialog):
    def __init__(self, email):
        super().__init__()
        self.email = email
        self.setWindowTitle("Reset Password")
        self.setGeometry(100, 100, 400, 300)
        layout = QtWidgets.QVBoxLayout()

        self.otp_input = QtWidgets.QLineEdit()
        self.otp_input.setPlaceholderText("Enter OTP")
        layout.addWidget(self.otp_input)

        self.verify_otp_button = QtWidgets.QPushButton("Verify OTP")
        self.verify_otp_button.clicked.connect(self.verify_otp)
        layout.addWidget(self.verify_otp_button)

        self.new_password_input = QtWidgets.QLineEdit()
        self.new_password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.new_password_input.setPlaceholderText("New Password")
        self.new_password_input.setEnabled(False)
        layout.addWidget(self.new_password_input)

        self.confirm_password_input = QtWidgets.QLineEdit()
        self.confirm_password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.confirm_password_input.setPlaceholderText("Confirm New Password")
        self.confirm_password_input.setEnabled(False)
        layout.addWidget(self.confirm_password_input)

        self.reset_password_button = QtWidgets.QPushButton("Reset Password")
        self.reset_password_button.clicked.connect(self.reset_password)
        self.reset_password_button.setEnabled(False)
        layout.addWidget(self.reset_password_button)

        self.setLayout(layout)

    def verify_otp(self):
        otp = self.otp_input.text()
        if otp:
            ref = db.reference('otps')
            otps = ref.order_by_child('email').equal_to(self.email).get()
            for otp_key, otp_value in otps.items():
                if otp_value['otp'] == otp:
                    QMessageBox.information(self, "OTP Verified", "OTP has been successfully verified.")
                    ref.child(otp_key).delete()
                    self.otp_input.setEnabled(False)
                    self.verify_otp_button.setEnabled(False)
                    self.new_password_input.setEnabled(True)
                    self.confirm_password_input.setEnabled(True)
                    self.reset_password_button.setEnabled(True)
                    return
            QMessageBox.warning(self, "Verification Failed", "Invalid OTP.")
        else:
            QMessageBox.warning(self, "Input Error", "OTP is required.")

    def reset_password(self):
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()
        if new_password and confirm_password:
            if new_password == confirm_password:
                hashed_password = hash_password(new_password)
                ref = db.reference('users').order_by_child('email').equal_to(self.email).get()
                for user_key, user_value in ref.items():
                    db.reference(f'users/{user_key}').update({'password': hashed_password})
                QMessageBox.information(self, "Success", "Password has been reset successfully.")
                self.accept()
            else:
                QMessageBox.warning(self, "Input Error", "Passwords do not match.")
        else:
            QMessageBox.warning(self, "Input Error", "Both fields are required.")

class AuthApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Application Title")
        self.setStyleSheet("background-color: #2b2b2b;")
        self.showFullScreen()
        main_layout = QtWidgets.QVBoxLayout()

        title_label = QtWidgets.QLabel("Welcome to Application!")
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 3vw; color: #FFFFFF; font-weight: bold;")
        main_layout.addWidget(title_label)

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background-color: #5A5A5A; 
                color: #FFFFFF; 
                padding: 1.5vw 2.5vw; 
                border-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #FFA500;
            }
            QTabBar::tab:hover {
                background-color: #FF8C00;
            }
        """)
        self.tabs.addTab(self.create_signup_tab(), "Sign Up")
        self.tabs.addTab(self.create_login_tab(), "Login")
        main_layout.addWidget(self.tabs)

        self.setLayout(main_layout)

    def create_signup_tab(self):
        signup_tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        self.signup_email = QtWidgets.QLineEdit()
        self.signup_email.setPlaceholderText("Email")
        self.signup_email.setMinimumWidth(350)
        self.signup_email.setMinimumHeight(35)

        signup_button = QtWidgets.QPushButton("Send OTP")
        signup_button.setMinimumHeight(50)
        signup_button.setStyleSheet(self.get_button_style())
        signup_button.clicked.connect(self.handle_signup)

        self.otp_input = QtWidgets.QLineEdit()
        self.otp_input.setPlaceholderText("OTP")
        self.otp_input.setMinimumHeight(35)
        self.otp_input.setStyleSheet(self.get_button_style())
        self.otp_input.setEnabled(False)

        verify_button = QtWidgets.QPushButton("Verify OTP")
        verify_button.setMinimumHeight(50)
        verify_button.setStyleSheet(self.get_button_style())
        verify_button.clicked.connect(self.handle_verification)
        verify_button.setEnabled(False)

        self.signup_password = QtWidgets.QLineEdit()
        self.signup_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.signup_password.setPlaceholderText("Password")
        self.signup_password.setMinimumHeight(35)
        self.signup_password.setEnabled(False)

        self.signup_password_confirm = QtWidgets.QLineEdit()
        self.signup_password_confirm.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.signup_password_confirm.setPlaceholderText("Confirm Password")
        self.signup_password_confirm.setMinimumHeight(35)
        self.signup_password_confirm.setEnabled(False)

        view_password_button_signup = QtWidgets.QPushButton("View Password")
        view_password_button_signup.setMinimumHeight(50)
        view_password_button_signup.setStyleSheet(self.get_button_style())
        view_password_button_signup.clicked.connect(lambda: self.toggle_password(self.signup_password))

        view_password_confirm_button_signup = QtWidgets.QPushButton("View Password Confirmation")
        view_password_confirm_button_signup.setMinimumHeight(50)
        view_password_confirm_button_signup.setStyleSheet(self.get_button_style())
        view_password_confirm_button_signup.clicked.connect(lambda: self.toggle_password(self.signup_password_confirm))

        final_signup_button = QtWidgets.QPushButton("Sign Up")
        final_signup_button.setMinimumHeight(50)
        final_signup_button.setStyleSheet(self.get_button_style())
        final_signup_button.clicked.connect(self.complete_signup)
        final_signup_button.setEnabled(False)

        layout.addWidget(self.signup_email)
        layout.addWidget(signup_button)
        layout.addWidget(self.otp_input)
        layout.addWidget(verify_button)
        layout.addWidget(self.signup_password)
        layout.addWidget(self.signup_password_confirm)
        layout.addWidget(view_password_button_signup)
        layout.addWidget(view_password_confirm_button_signup)
        layout.addWidget(final_signup_button)
        signup_tab.setLayout(layout)

        self.signup_button = signup_button
        self.verify_button = verify_button
        self.final_signup_button = final_signup_button

        return signup_tab

    def create_login_tab(self):
        login_tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        self.login_email = QtWidgets.QLineEdit()
        self.login_email.setPlaceholderText("Email")
        self.login_email.setMinimumHeight(35)
        self.login_password = QtWidgets.QLineEdit()
        self.login_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.login_password.setPlaceholderText("Password")
        self.login_password.setMinimumHeight(35)

        view_password_button_login = QtWidgets.QPushButton("View Password")
        view_password_button_login.setStyleSheet(self.get_button_style())
        view_password_button_login.setMinimumHeight(50)
        view_password_button_login.clicked.connect(lambda: self.toggle_password(self.login_password))

        login_button = QtWidgets.QPushButton("Login")
        login_button.setStyleSheet(self.get_button_style())
        login_button.setMinimumHeight(50)
        login_button.clicked.connect(self.login_with_access_code)

        request_login_button = QtWidgets.QPushButton("Request Login")
        request_login_button.setStyleSheet(self.get_button_style())
        request_login_button.setMinimumHeight(50)
        request_login_button.clicked.connect(self.handle_request_login)

        forgot_password_button = QtWidgets.QPushButton("Forgot Password?")
        forgot_password_button.setStyleSheet(self.get_button_style())
        forgot_password_button.setMinimumHeight(50)
        forgot_password_button.clicked.connect(self.handle_forgot_password)

        self.access_code_button = QtWidgets.QPushButton("Enter Access Code")
        self.access_code_button.setStyleSheet(self.get_button_style())
        self.access_code_button.setMinimumHeight(50)
        self.access_code_button.clicked.connect(self.open_access_code_dialog)
        self.access_code_button.setEnabled(False)

        layout.addWidget(self.login_email)
        layout.addWidget(self.login_password)
        layout.addWidget(view_password_button_login)
        layout.addWidget(login_button)
        layout.addWidget(request_login_button)
        layout.addWidget(forgot_password_button)
        layout.addWidget(self.access_code_button)
        login_tab.setLayout(layout)

        return login_tab

    def toggle_password(self, field):
        if field.echoMode() == QtWidgets.QLineEdit.EchoMode.Password:
            field.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            field.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def handle_signup(self):
        email = self.signup_email.text()
        if email:
            send_otp(email)
            QMessageBox.information(self, "OTP Sent", "An OTP has been sent to your email.")
            self.signup_button.setEnabled(False)
            self.otp_input.setEnabled(True)
            self.verify_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "Input Error", "Email is required.")

    def handle_verification(self):
        email = self.signup_email.text()
        otp = self.otp_input.text()
        if email and otp:
            ref = db.reference('otps')
            otps = ref.order_by_child('email').get()
            for otp_key, otp_value in otps.items():
                if otp_value['email'] == email and otp_value['otp'] == otp:
                    QMessageBox.information(self, "OTP Verified", "OTP has been successfully verified.")
                    ref.child(otp_key).delete()
                    self.otp_input.setEnabled(False)
                    self.verify_button.setEnabled(False)
                    self.signup_password.setEnabled(True)
                    self.signup_password_confirm.setEnabled(True)
                    self.final_signup_button.setEnabled(True)
                    return
            QMessageBox.warning(self, "Verification Failed", "Invalid OTP.")
        else:
            QMessageBox.warning(self, "Input Error", "Email and OTP are required.")

    def complete_signup(self):
        email = self.signup_email.text()
        password = self.signup_password.text()
        password_confirm = self.signup_password_confirm.text()
        if email and password and password_confirm:
            if password == password_confirm:
                hashed_password = hash_password(password)
                ref = db.reference('users')
                ref.push({
                    'email': email,
                    'password': hashed_password
                })
                QMessageBox.information(self, "Sign Up Successful", "Your account has been created successfully.")
                self.signup_email.clear()
                self.otp_input.clear()
                self.signup_password.clear()
                self.signup_password_confirm.clear()
                self.signup_button.setEnabled(True)
                self.otp_input.setEnabled(False)
                self.verify_button.setEnabled(False)
                self.signup_password.setEnabled(False)
                self.signup_password_confirm.setEnabled(False)
                self.final_signup_button.setEnabled(False)
            else:
                QMessageBox.warning(self, "Input Error", "Passwords do not match.")
        else:
            QMessageBox.warning(self, "Input Error", "All fields are required.")

    def handle_request_login(self):
        email = self.login_email.text()
        password = self.login_password.text()

        if not email or not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Both fields are required!")
            return

        password_hash = hash_password(password)
        ref = db.reference('users').order_by_child('email').equal_to(email).limit_to_last(1).get()
        user_data = next(iter(ref.values()), None)

        print(f"user_data: {user_data}")

        if user_data and user_data.get('password') == password_hash:
            response = requests.post('http://127.0.0.1:5000/request_approval', json={'email': email})
            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Info", "Login request sent to superadmin for approval.")
                self.access_code_button.setEnabled(True)
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to send approval request.")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid email or password.")

    def login_with_access_code(self):
        email = self.login_email.text()
        password = self.login_password.text()

        if not email or not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Both fields are required!")
            return

        password_hash = hash_password(password)
        ref = db.reference('users').order_by_child('email').equal_to(email).limit_to_last(1).get()
        user_data = next(iter(ref.values()), None)

        print(f"user_data: {user_data}")

        if user_data and user_data.get('password') == password_hash:
            self.access_code_button.setEnabled(True)
            self.open_access_code_dialog()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid email or password.")

    def open_access_code_dialog(self):
        dialog = AccessCodeDialog()
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            access_code = dialog.access_code_input.text()
            email = self.login_email.text()

            if access_code and email:
                try:
                    ref = db.reference('access_codes')
                    access_codes = ref.order_by_child('email').equal_to(email).get()
                    for code_key, code_value in access_codes.items():
                        if code_value['access_code'] == access_code:
                            expiry_time = parser.isoparse(code_value['expiry_time'])
                            if datetime.utcnow() <= expiry_time:
                                self.main_page = MainPage()
                                self.main_page.show()
                                self.close()
                                return
                    QtWidgets.QMessageBox.warning(self, "Error", "Invalid or expired access code.")
                except firebase_admin.exceptions.InvalidArgumentError as e:
                    QtWidgets.QMessageBox.warning(self, "Error", f"Firebase error: {e}")
                except Exception as e:
                    QtWidgets.QMessageBox.warning(self, "Error", f"Unexpected error: {e}")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Email and access code are required.")

    def handle_forgot_password(self):
        email = self.login_email.text()
        if not email:
            QtWidgets.QMessageBox.warning(self, "Error", "Email is required to reset password.")
            return

        send_otp(email)
        QMessageBox.information(self, "OTP Sent", "An OTP has been sent to your email.")
        dialog = ResetPasswordDialog(email)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            QtWidgets.QMessageBox.information(self, "Success", "Password has been reset successfully.")

    def get_button_style(self):
        return """
            QPushButton {
                background-color: #5A5A5A; 
                color: #FFFFFF; 
                padding: 1.5vw 2.5vw; 
                border-radius: 5px;
                font-size: 1vw;
            }
            QPushButton:hover {
                background-color: #FFA500;
            }
            QPushButton:pressed {
                background-color: #FF8C00;
            }
        """

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = AuthApp()
    window.show()
    app.exec()
