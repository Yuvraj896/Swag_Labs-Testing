class Example {
    private:
        int secret;
    public:    
    
        void setSecret(int value) {
             secret = value;   }
             
        int getSecret() {
            return secret;   
        }
    };
    
    int main() { Example obj;   obj.setSecret(42);18    std::cout << obj.getSecret();19    return 0;20}