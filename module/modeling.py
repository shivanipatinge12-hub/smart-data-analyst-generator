from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, r2_score
def train_models(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    results = {}
    if y.dtype == "object" or y.nunique() < 10:
        problem_type = "classification"
    else:
        problem_type = "regression"
    if problem_type == "classification":
        models = {
            "Logistic Regression": Pipeline([
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(max_iter=2000))
            ]),
            "Decision Tree": DecisionTreeClassifier(),
            "KNN": Pipeline([
                ("scaler", StandardScaler()),
                ("model", KNeighborsClassifier())
            ])
        }
    else:
        models = {
            "Linear Regression": LinearRegression(),
            "Decision Tree Regressor": DecisionTreeRegressor(),
            "KNN Regressor": Pipeline([
                ("scaler", StandardScaler()),
                ("model", KNeighborsRegressor())
            ])
        }
    for name, model in models.items():
        try:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            if problem_type == "classification":
                score = accuracy_score(y_test, y_pred)
            else:
                score = r2_score(y_test, y_pred)
            results[name] = round(score, 4)
        except Exception as e:
            results[name] = f"Error: {str(e)}"
    return results