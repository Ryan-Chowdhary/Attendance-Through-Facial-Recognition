#include <iostream>
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/objdetect.hpp>
#include <thread>
#include <mutex>

using namespace cv;
double scalefactor = 1.0; // Scale factor for frame resizing
const auto path = 0; // Path to video Source
int neighbours = 7; // minimum number of neighbours required for detection

Mat frame, grayframe;
Mat *pFrame = &frame;
Mat *pGrayframe = &grayframe;

VideoCapture cap(path);
CascadeClassifier faceCascade;
std::vector<Rect> faces;
Mutex m;

void detect();
void show();

int main()
{
    // All frames shall be read directly from source
    cap.set(CAP_PROP_BUFFERSIZE, 0); // Set Buffer size to zero
    
    faceCascade.load("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml");
    if (faceCascade.empty())
    {
        std::cout << "xml was not loaded" << "\n";
        return -1;
    }
    // Set Vector to empty
    faces.clear();
    // Call FaceCascade to detect faces in frame 
    // in parallel to the rest of the program for better framerate
    std::thread ts(show), td(detect);
    ts.join();
    td.join();
    return -1;
}

void detect()
{
    std::vector<Rect> temp_faces;
    while (true)
    {
        if (!pFrame->empty())
        {
            cvtColor(*pFrame, *pGrayframe, COLOR_BGR2GRAY);
            resize(*pGrayframe, *pGrayframe, Size(pGrayframe->size().width / scalefactor, pGrayframe->size().height / scalefactor), INTER_LINEAR_EXACT);
            faceCascade.detectMultiScale(*pGrayframe, temp_faces, 1.05, neighbours, 0, Size());
            m.lock();
            faces = temp_faces; // Vector is copied through '=' operator
            m.unlock();
        }
    }
}

void show()
{
    while (true)
    {
        if (!cap.isOpened())
        {
            break;
        }
        while (true)
        {
            m.lock();
            cap >> *pFrame;
            m.unlock();
            if (pFrame->empty())
            {
                break;
            }
            for (int i = 0; i < faces.size(); i++)
            {
                rectangle(*pFrame, faces[i].br(), faces[i].tl(), Scalar(255, 0, 255), 3);
            }
            imshow("Video", *pFrame);
            waitKey(10);
        }
        std::cout << "empty frame" << std::endl;
        break;
    }
}