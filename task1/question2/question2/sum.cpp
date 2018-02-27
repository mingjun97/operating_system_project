#include "sum.h"
#include "ui_sum.h"
#include <QTimer>
#include <QStringListModel>

sum::sum(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::sum)
{
    ui->setupUi(this);
    this->result = 0;
    this->mid = 1;
    this->timer = new QTimer(this);
    connect(this->timer,SIGNAL(timeout()),this,SLOT(getsum()));
    timer->start(250);
}

sum::~sum()
{
    delete ui;
}

void sum::getsum(){
    this->result += this->mid++;
    this->ui->output->insertItem(999999, QString::number(this->result));
    if (mid >= 1000) {
        this->timer->stop();
    }
}
