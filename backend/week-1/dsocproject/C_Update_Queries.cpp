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
        for ( int i = 0; i<m; i++) cin >> x;
        string c;
        cin >> c;
        int arr[27] = {0};
        for ( int i = 0; i<c.size(); i++){
            arr[c[i] - 'a']++;
        }
        for ( int i = 0; i<n; i++){
            for ( int j =0; j<26; j++){
                if (arr[j]!=0){
                    if ((s[i]-'a') > j){
                        s[i] = (char)('a'+j);
                        arr[j]--;
                        break;
                    }
                }
            }
        }
        cout << s << endl;
    }
}