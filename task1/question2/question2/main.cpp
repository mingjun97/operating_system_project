#include "mainwindow.h"
#include <QApplication>
#include "show_file.h"
#include "sum.h"


int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    show_file h;
    h.show();
    MainWindow w;
    w.show();
    sum s;
    s.show();

    /**
        pid_t p1,p2;
        if (p1 = fork() == 0){
            show_file h;
            h.show();
        }else if (p2 = fork() == 0){
            MainWindow w;
            w.show();
        }else{
            sum s;
            s.show();
        }
    **/

    return a.exec();
}
