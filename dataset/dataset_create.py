from datasets import load_dataset

# dataset = load_dataset("json", data_files="/home/hz1/rzhong/dataset/wechatarticle_dataset/dataset_info.json")
dataset = load_dataset("/home/hz1/rzhong/dataset/wechatarticle_dataset")
print(dataset)
print(dataset["train"])
print(dataset["train"][0])
dataset["train"].to_parquet("./wechatarticle/")