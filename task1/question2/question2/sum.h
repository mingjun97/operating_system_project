#ifndef SUM_H
#define SUM_H

#include <QMainWindow>
#include <QStringListModel>
#include <QTimer>

namespace Ui {
class sum;
}

class sum : public QMainWindow
{
    Q_OBJECT

public:
    explicit sum(QWidget *parent = 0);
    ~sum();

private:
    Ui::sum *ui;
    int mid, result;
    QStringListModel *m_model;
    QTimer *timer;

private slots:
    void getsum(void);
};

#endif // SUM_H
