
# Caffe network training tools


Recently I was trying to build a neural net work.

Since my data source are images, so I gave a shoot on caffe. And I have to say it's very unfriendly to a beginner. I spent almost a whole week to figure out how to transform images
to lmdb files that caffe could use for training, and how to deploy a trained network.

And I wrote a tool to generate all the file you need for training and deploying (except network structure and solver config), all you need to do is change config.py and run preprocess.py.

I can use it generate what I need quickly instead of run some bash script in example file.

#      

If you want to go further, you can run train.py which will train network automatically after generating files above, which is recommended.

One thing have to be mentioned is carefully edit config.py, solver.prototxt and architecture.prototxt. Any improper setting will result in running error.

#    

Run  /test/test.py  to check if your environment is good to go.

(Please specify valid caffe (master&tools) path and pycaffe path first.)

(If you want to run GPU tset, use "test.py --gpu gpu_id" to do so.)
#     

Anyway, I hope it can help you.

Happy machine learning~

#  

If you have any advice, please contact me.

haojie.d.yuan@gmail.com

HaojieYuan at Sep 14, 2017
