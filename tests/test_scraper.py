from app.tools import scraper


def test_batch_egenration():
    dataset = [0, 1, 2, 3, 4]
    batches = [batch for batch in scraper.batch(dataset, 3)]
    assert batches[0] == ([0, 1, 2], 0)
    assert batches[1] == ([3, 4], 3)
