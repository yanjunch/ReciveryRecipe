from foodcom import FoodCom
from googlemap import GoogleMap
from foodkeeper import FoodKeeper


class Reciveray(object):
    def __init__(self, online_mode):
        self.online_mode = online_mode
        self.FoodCom = FoodCom(self.online_mode)
        self.GoogleMap = GoogleMap(self.online_mode)
        self.FoodKeeper = FoodKeeper(self.online_mode)
        
    def food_recommend(self):        
        return self.FoodCom.rank_page()
    
    def search(self, keywords):
        return self.FoodCom.search(keywords)
    
    def workflow(self):
        
        tag = input("\nDo you want to search a specific dish or our recommended dishes？S/R: ")
        recommendation_mode = tag == 'R'
        
        # recommend dish
        if(recommendation_mode):
            try:
                recommendation_dic = self.food_recommend()
                print(recommendation_dic)
                tag = input("\nDo you want to see other recommendation? Y/N: ")
                next_page_tag = tag == "Y"
                while(next_page_tag):
                    recommendation_dic.update(self.food_recommend())
                    print(recommendation_dic)
                    tag = input("\nDo you want to see other recommendation? Y/N: ")
                    next_page_tag = tag == "Y"
            except:
                print("\nTODO: recommend dish") 
                     
        else: 
        # search dish
            keywords = input("\nPlease input any dish you want to search: ")
            try:
                search_dic = self.search(keywords)
                print(search_dic)
                tag = input("\nDo you want to see next page？Y/N: ")
                next_page_tag = tag == "Y"
                while(next_page_tag):
                    search_dic.update(self.search(keywords))
                    print(search_dic)
                    tag = input("\nDo you want to see other recommendation? Y/N: ")
                    next_page_tag = tag == "Y"
            except:
                print("TODO: search dish") 
            
        # display dish
        dish_id = input("\nChoose the recipy you want to see detail？Only Number: ")
        # dish_id = eval(dish_id)
        dish_id = str(dish_id)
        self.FoodCom.dish_id = dish_id
        try:
            self.FoodCom.one_recipe_detail(dish_id)
        except:
            print("\nTODO: display dish") 
            
        # bug ingredient
        tag = input("\nDo you want to buy the ingredients and try it? Y/N: ")
        buy_tag = tag == "Y"
        if(buy_tag):
            post_code = input("\nPlease input your post code so that we can recommend the best grocery stores for you: ")
            post_code = eval(post_code)
            
            try:
                grocery_dic = self.GoogleMap.search(post_code)
                print(grocery_dic)
                
                grocery_id = input("\nChoose the recipy you want to see detail？Only Number: ")
                grocery_id = eval(grocery_id)
                
            except:
                print("\nTODO: bug ingredient") 
            
            print("\nYour order has been confirmed.")  
                    
        # display food keep advise
        tag = input("\nDo you want to know how to keep the ingredients? Y/N: ")
        food_keeper_tag = tag == "Y"
        if(food_keeper_tag):
            try:
                print(self.FoodCom.display_ingredients())
                ingredient_id = input("\nChoose the ingredient you want to see detail？Only Number: ")
                ingredient_id = eval(ingredient_id)
                print(self.FoodCom.display_ingredients(ingredient_id)) 
            except:
                print("\nTODO: display food keep advise")
                
        print("\nThanks for using!")
    

if __name__ == '__main__':

    reciveray =  Reciveray(online_mode=False)
    reciveray.workflow()
    

