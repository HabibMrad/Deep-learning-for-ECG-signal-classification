xx=imread('1.jpg'); %����һ������ɫ��ͼƬ
xxgray=rgb2gray(xx);     %����ת��Ϊ�Ҷ�ֵ
cmap=colormap;            %��õ�ǰɫ��
xxcolormap=rgb2ind(xx,cmap); %��xxת��Ϊ0~1��ɫ��ֵ������
xxgray=double(xxgray);   %������ֵԭ��Ϊunit8������ֵ
xxcolormap=double(xxcolormap);  %��mesh��Ҫdouble���ͣ���תһ������
figure
mesh(xxgray,xxcolormap);   %�����͵õ�һ���лҶȾ����ߵͣ�ԭͼ��ɫ���ǵ���άͼ��