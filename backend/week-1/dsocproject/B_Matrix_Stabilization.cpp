#include <bits/stdc++.h>
using namespace std;

int main(){
    int t;
    cin >> t;
    while (t--){
        int n , m;
        cin >> n >> m;
        string s;
        cin >> s;
        int x;
                set<int> arr1;
        for ( int i = 0; i<m; i++) {cin >> x; arr1.insert(x);}
        string c;
        cin >> c;
        sort(c.begin() , c.end());
        int i = 0;
        for (auto e : arr1){
            s[e-1] = c[i];
            i++;
        }
        cout << s << endl;
    }
}