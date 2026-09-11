import pandas as pd
from collections import defaultdict, deque
import heapq


class FriendGraph:

    def __init__(self):
        # graph[A][B] = friendship weight
        self.graph = defaultdict(dict)

    # --------------------------------------------------
    # 1. ADD FRIENDSHIP
    # --------------------------------------------------
    def add_friendship(self, person1, person2, weight):
        self.graph[person1][person2] = weight
        self.graph[person2][person1] = weight

    # --------------------------------------------------
    # 2. LOAD GRAPH FROM CSV
    # --------------------------------------------------
    def load_csv(self, filename="friend.csv"):
        df = pd.read_csv(filename)

        for _, row in df.iterrows():
            person = str(row["person"]).strip()
            friend = str(row["friend"]).strip()
            weight = float(row["weight"])

            self.add_friendship(person, friend, weight)

    # --------------------------------------------------
    # 3. BFS TRAVERSAL
    # --------------------------------------------------
    def bfs(self, start):
        if start not in self.graph:
            return []

        visited = set()
        queue = deque([start])
        traversal = []

        visited.add(start)

        while queue:
            current = queue.popleft()
            traversal.append(current)

            for friend in self.graph[current]:
                if friend not in visited:
                    visited.add(friend)
                    queue.append(friend)

        return traversal

    # --------------------------------------------------
    # 4. DFS TRAVERSAL
    # --------------------------------------------------
    def dfs(self, start):
        if start not in self.graph:
            return []

        visited = set()
        traversal = []

        def dfs_recursive(current):
            visited.add(current)
            traversal.append(current)

            for friend in self.graph[current]:
                if friend not in visited:
                    dfs_recursive(friend)

        dfs_recursive(start)

        return traversal

    # --------------------------------------------------
    # 5. SHORTEST PATH USING DIJKSTRA
    # --------------------------------------------------
    def shortest_path(self, start, target):

        if start not in self.graph or target not in self.graph:
            return None

        distance = {
            node: float("inf")
            for node in self.graph
        }

        distance[start] = 0
        previous = {}

        pq = [(0, start)]

        while pq:

            current_distance, current = heapq.heappop(pq)

            if current_distance > distance[current]:
                continue

            if current == target:
                break

            for friend, weight in self.graph[current].items():

                new_distance = current_distance + weight

                if new_distance < distance[friend]:

                    distance[friend] = new_distance
                    previous[friend] = current

                    heapq.heappush(
                        pq,
                        (new_distance, friend)
                    )

        if distance[target] == float("inf"):
            return None

        # Reconstruct path
        path = []
        current = target

        while current != start:
            path.append(current)
            current = previous[current]

        path.append(start)
        path.reverse()

        return {
            "path": path,
            "distance": distance[target]
        }

    # --------------------------------------------------
    # 6. FRIEND RECOMMENDATION
    # --------------------------------------------------
    def recommend_friends(self, host, top_n=5):

        if host not in self.graph:
            return []

        direct_friends = set(
            self.graph[host].keys()
        )

        recommendations = defaultdict(lambda: {
            "score": 0,
            "mutual_friends": []
        })

        # Host -> Mutual Friend -> Candidate
        for mutual_friend, host_weight in self.graph[host].items():

            for candidate, friend_weight in self.graph[mutual_friend].items():

                # Don't recommend host
                if candidate == host:
                    continue

                # Don't recommend existing friends
                if candidate in direct_friends:
                    continue

                # Recommendation score
                score = host_weight * friend_weight

                recommendations[candidate]["score"] += score

                recommendations[candidate]["mutual_friends"].append(
                    mutual_friend
                )

        results = []

        for candidate, data in recommendations.items():

            results.append({
                "candidate": candidate,
                "score": data["score"],
                "mutual_friends": data["mutual_friends"]
            })

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results[:top_n]


# ======================================================
# MAIN PROGRAM
# ======================================================

graph = FriendGraph()

# CSV FILE PATH
csv_file = "D:\\C\\Python\\friend.csv"

# Load CSV
graph.load_csv(csv_file)


# ======================================================
# BFS
# ======================================================

host = "Avinash"

print("\n========== BFS ==========")

bfs_result = graph.bfs(host)

print(" -> ".join(bfs_result))


# ======================================================
# DFS
# ======================================================

print("\n========== DFS ==========")

dfs_result = graph.dfs(host)

print(" -> ".join(dfs_result))


# ======================================================
# SHORTEST PATH
# ======================================================

target = "Rohit"

print("\n========== SHORTEST PATH ==========")

result = graph.shortest_path(host, target)

if result:

    print("Path:")
    print(" -> ".join(result["path"]))

    print("Total Weight:", result["distance"])

else:
    print("No path found.")


# ======================================================
# FRIEND RECOMMENDATIONS
# ======================================================

print("\n========== FRIEND RECOMMENDATIONS ==========")

suggestions = graph.recommend_friends(
    host,
    top_n=5
)

for i, suggestion in enumerate(suggestions, start=1):

    print(f"{i}. {suggestion['candidate']}")
    print(f"   Score: {suggestion['score']}")
    print(
        f"   Mutual Friends: "
        f"{', '.join(suggestion['mutual_friends'])}"
    )
