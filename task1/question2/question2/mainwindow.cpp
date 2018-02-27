#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QTimer>
#include <QDateTime>
MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
        ui->setupUi(this);
        this->updatetime();
        QTimer *timer = new QTimer(this);
        connect(timer,SIGNAL(timeout()),this,SLOT(updatetime()));
        timer->start(1000);
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::updatetime(){
    QDateTime time = QDateTime::currentDateTime();
    QString str = time.toString("yyyy-MM-dd hh:mm:ss dddd");
    ui->label_2->setText(str);
}
