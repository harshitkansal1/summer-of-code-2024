#include <bits/stdc++.h>
using namespace std;

int main(){
    int t;
    cin >> t;
    while (t--){
        int n;
        cin >> n;
        string s;
        cin >> s;
        int arr[n];
        if (n ==2) {
            cout << (s[0]-'0')*10 + (s[1]-'0') << endl;
            continue;
        }
        for ( int i = 0; i<n; i++) arr[i] =s[i]-'0';
        if (n == 3 ){
            int a1 = arr[0]*(arr[1]*10 + arr[2]);
            int a2 =  arr[0]+(arr[1]*10 + arr[2]);
            int a3 =  arr[2]*(arr[0]*10 + arr[1]);
             int a4 = arr[2]+(arr[0]*10 + arr[1]);
            a1 = min(a1 , a2);
                        a1 = min(a1 , a3);

            a1 = min(a1 , a4);
            cout << a1 << endl;
            continue;
        }
        int temp = false;
        for ( int i=  0; i<n; i++) if (arr[i] == 0){cout << 0 << endl; temp = true; break;}
        if (temp) continue;
        int ans = 0;
        int mini = *min_element(arr , arr+n-1);
        for ( int i = 0; i<n; i++){
            if (arr[i]!=1)ans+=arr[i];
        }
        bool temp2 = false;
        if (mini == 1){
            ans+=10;
        }
        else ans+=(mini*9);
        for ( int i =0; i<n-1; i++){if (arr[i] == mini && arr[i+1]!=1) temp2 = true;}
        if (!temp2)ans+=1;
        cout << ans << endl;
    }
}