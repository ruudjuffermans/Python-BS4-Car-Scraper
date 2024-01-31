from src.etl import ETLCarModels, ETLCarShallows, ETLCarListings
import time


if __name__ == "__main__":
    # etl = ETLCarModels()
    # etl.run()

    while True:
        etl = ETLCarShallows()
        etl.run()  

        
    # while True:

    #     etl = ETLCarListings()
    #     etl.run()
    #     time.sleep(2)

