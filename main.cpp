#include <iostream>
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/objdetect.hpp>

using namespace cv;
double scalefactor = 1.0;
const auto path = 0;
int samplenum = 1;
std::mutex m;

Mat frame, grayframe;
Mat *pFrame = &frame;
Mat *pGrayframe = &grayframe;

VideoCapture cap(path);
CascadeClassifier faceCascade;
std::vector<Rect> faces;

int main()
{
    cap.set(CAP_PROP_BUFFERSIZE, 0);
    faceCascade.load("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml");
    if (faceCascade.empty())
    {
        std::cout << "xml was not loaded" << "\n";
        return -1;
    }
    faces.clear();
    while (true)
    {
        if (!cap.isOpened())
        {
            break;
        }
        cap >> *pFrame;
        if (pFrame->empty())
        {
            std::cout << "empty frame" << std::endl;
            return -1;
        }
        cvtColor(*pFrame, *pGrayframe, COLOR_BGR2GRAY);
        resize(*pGrayframe, *pGrayframe, Size(pGrayframe->size().width / scalefactor, pGrayframe->size().height / scalefactor), INTER_LINEAR_EXACT);
        faceCascade.detectMultiScale(*pGrayframe, *&faces, 1.08, 5, 0, Size(30, 30));
        for (int i = 0; i < faces.size(); i++)
        {
            rectangle(*pFrame, faces[i].tl(), faces[i].br(), Scalar(255, 0, 255), 3);
        }
        imshow("Video", *pFrame);
        waitKey(10);
    }
    return -1;
}