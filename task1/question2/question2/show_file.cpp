#include "show_file.h"
#include "ui_show_file.h"
#include <stdio.h>
#include <QFile>
#include <QTimer>


show_file::show_file(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::show_file)
{
    ui->setupUi(this);
    this->updatecontent();
    QTimer *timer = new QTimer(this);
    connect(timer,SIGNAL(timeout()),this,SLOT(updatecontent()));
    timer->start(1000);
}

show_file::~show_file()
{
    delete ui;
}

void show_file::updatecontent(){
    QFile *file=new QFile(ui->src->text());
    file->open(QIODevice::ReadOnly|QIODevice::Text);
    QString data = QString(file->readAll());
    ui->text->setText(data);
}
