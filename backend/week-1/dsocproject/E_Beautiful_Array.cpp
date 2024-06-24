#include <bits/stdc++.h>
using namespace std;
#define int long long

int32_t main(){
    int t;
    cin >> t;
    while (t--){
        int n ,k;
        cin >> n >> k;
        vector<int> v(n , 0);
        for ( int i = 0;i<n; i++) cin >> v[i];
        vector<pair<int , int>> diff;
        for ( int i = n-1; i>=0; i--){
            diff.push_back({(v[i])%k , v[i]});
        }
        if (n ==1){
            cout << 0 << endl; continue;
        }
        sort(diff.begin() , diff.end());
        vector<vector<int>> temp;
        vector<int> temp2;
        temp2.push_back(diff[0].second);
        for ( int i = 1; i<n; i++){
            if (diff[i].first == diff[i-1].first) temp2.push_back(diff[i].second);
            else {
                temp.push_back(temp2);
                temp2.clear();
                temp2.push_back(diff[i].second);
            }
        }
        temp.push_back(temp2);
        bool ans = true;
        for (auto e : temp){
            if (e.size()%2==1) ans = false;
        }
                int num = 0;
        if (n%2 == 0){ if (!ans){cout << -1 << endl; continue;}
        else {
            for (auto e : temp){
                for ( int i = 1; i<e.size(); i = i+2){
                    num+=(e[i] - e[i-1])/k;
                }
            }
            cout << num << endl;
        }}
       

    }


}