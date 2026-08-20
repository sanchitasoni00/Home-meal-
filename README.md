# HomeMeal — Member 5 Recommendation Engine

This is the complete beginner-friendly Member 5 MVP described in the project
guide.

## Folder structure

```text
HomeMeal/
├── app.py
├── recommendation.py
├── requirements.txt
└── data/
    └── cooks.json
```

## 1. Install Python

Use Python 3.10+.

## 2. Open the project in VS Code

Open this folder:

```text
HomeMeal_Member5_Recommendation
```

## 3. Install dependencies

Open the VS Code terminal:

```bash
pip install -r requirements.txt
```

## 4. Run the website

```bash
streamlit run app.py
```

A browser window should open with the HomeMeal recommendation page.

## 5. What the code does

The student enters:

- Budget
- Meal type
- Food preference
- Spice level

Each cook is then scored using:

- Price match: 25 points
- Food preference match: 25 points
- Meal match: 20 points
- Rating: 15 points
- Distance: 15 points

Maximum = 100 points.

The cooks are sorted from the highest score to the lowest score and the top
three are displayed.

## 6. Important note about spice level

The project guide requires spice level as an input, but its specified
100-point model does not give spice level a numerical weight. Therefore this
implementation collects spice level and reports whether it matches without
changing the official 100-point scoring model.

## 7. GitHub

After testing:

```bash
git init
git add .
git commit -m "Add HomeMeal recommendation engine"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Member 1 can then copy/import `recommendation.py` into the main HomeMeal
application and Member 4 can replace `data/cooks.json` with the team's shared
cook data.
