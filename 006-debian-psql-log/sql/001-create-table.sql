SET search_path TO aaa;

CREATE TABLE events (
    run_id INT, 
    message TEXT,
    insert_ts TIMESTAMP DEFAULT now()
);

CREATE TABLE status (
	status TEXT DEFAULT 'not ready'
);
